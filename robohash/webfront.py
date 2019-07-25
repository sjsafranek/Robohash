#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

# Find details about this project at https://github.com/e1ven/robohash

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import hashlib
import random
from robohash import Robohash
from robohash import SETS
from robohash import BGSETS
import io
import base64
import json

# Import urllib stuff that works in both Py2 and Py3
try:
    import urllib.request
    import urllib.parse
    urlopen = urllib.request.urlopen
    urlencode = urllib.parse.urlencode
except ImportError:
    import urllib2
    import urllib
    urlopen = urllib2.urlopen
    urlencode = urllib.urlencode

from tornado.options import define, options
import io

import logger
log = logger.log

define("port", default=80, help="run on the given port", type=int)



class ImageSetsHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(200)
        self.set_header("Content-Type", "application/json")
        self.write(
            json.dumps({
                "status": "ok",
                "data": {
                    "sets": SETS
                }
            })
        )


class ImageBackgroundSetsHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(200)
        self.set_header("Content-Type", "application/json")
        self.write(
            json.dumps({
                "status": "ok",
                "data": {
                    "sets": BGSETS
                }
            })
        )


class ImageHandler(tornado.web.RequestHandler):

    def getImageSize(self):
        # Set default values
        defaultSizeX = 300
        defaultSizeY = 300
        defaultSize = '300x300'

        # Split the size variable in to sizex and sizey
        imageSize = self.get_argument('size', defaultSize, True)
        if str != type(imageSize):
            imageSize = imageSize.decode('utf-8')

        sizex, sizey = imageSize.split("x")
        sizex = int(sizex)
        sizey = int(sizey)
        if sizex > 4096 or sizex < 0:
            sizex = defaultSizeX
        if sizey > 4096 or sizey < 0:
            sizey = defaultSizeY

        return sizex, sizey

    def getImageSet(self, choices=[]):
        # Allow users to manually specify a robot 'set' that they like.
        # Ensure that this is one of the allowed choices, or allow all
        # If they don't set one, take the first entry from sets above.
        imageSet = self.get_argument('set')
        if str != type(imageSet):
            imageSet = imageSet.decode('utf-8')
        return imageSet

    def get(self, string=None):
        """
        The ImageHandler is our tornado class for creating a robot.
        called as Robohash.org/$1, where $1 becomes the seed string for the Robohash obj
        """

        # Ensure we have something to hash!
        if string is None:
            string = self.request.remote_ip

        # Set default values
        imageFormat = self.get_argument('format', 'png', True).upper()
        sizex, sizey = self.getImageSize()

        # Allow Gravatar lookups -
        # This allows people to pass in a gravatar-style hash, and return their gravatar image, instead of a Robohash.
        # This is often used for example, to show a Gravatar if it's set for an email, or a Robohash if not.
        gravatar = self.get_argument('gravatar','').lower()
        if gravatar:
            if gravatar == 'yes':
                # They have requested that we hash the email, and send it to Gravatar.
                gravatar_url = "https://secure.gravatar.com/avatar/" + hashlib.md5(string.lower().encode('utf-8')).hexdigest() + "?"
                gravatar_url += urlencode({'size':str(sizey)})
            elif gravatar == 'hashed':
                # They have sent us a pre-hashed email address.
                gravatar_url = "https://secure.gravatar.com/avatar/" + string + "?"
                gravatar_url += urlencode({'size':str(sizey)})

            # If we do want a gravatar, request one. If we can't get it, just keep going, and return a robohash
            if gravatar in ['hashed','yes']:
                try:
                    print(gravatar_url)
                    f = urlopen(gravatar_url)
                    self.redirect(gravatar_url, permanent=False)
                    return
                except Exception as e:
                    print(e)

        # Detect if the user has passed in a flag to ignore extensions.
        # Pass this along to to Robohash obj later on.
        # ignoreext = self.get_argument('ignoreext', 'false', True).lower() == 'true'

        # Create our Robohashing object
        r = Robohash(string)

        # Get image set
        roboset = None
        imageSet = self.getImageSet()
        if not imageSet:
            roboset = r.sets[0]
        if imageSet in r.sets:
            roboset = imageSet
        elif imageSet == 'any':
            # Add ugly hack.
            # Adding cats and people per submitted/requested code, but I don't want to change existing hashes for set=any
            # so we'll ignore those sets for the 'any' config.
            roboset = r.sets[r.hasharray[1] % (len(r.sets)-2) ]
        else:
            self.set_status(404)
            self.set_header("Content-Type", "application/json")
            self.write('{"status":"error","error":"Not Found", "message": "set='+imageSet+' not found."}')
            return

        # Allow them to set a background, or keep as None
        bgset = self.get_argument('bgset', None, True)
        if bgset:
            if str != type(bgset):
                bgset = bgset.decode('utf-8')
            elif bgset not in r.bgsets + ['any']:
                self.set_status(404)
                self.set_header("Content-Type", "application/json")
                self.write('{"status":"error","error":"Not Found", "message": "bgset='+bgset+' not found."}')
                return

        # We're going to be returning the image directly, so tell the browser to expect a binary.
        self.set_header("Content-Type", "image/" + imageFormat)
        self.set_header("Cache-Control", "public,max-age=31536000")

        # Build our Robot.
        r.assemble(roboset=roboset, format=imageFormat, bgset=bgset, sizex=sizex, sizey=sizey)

        # # Print the Robot to the handler, as a file-like obj
        if r.format != 'datauri':
            r.img.save(self, format=r.format)
        else:
            # Or, if requested, base64 encode first.
            fakefile = io.BytesIO()
            r.img.save(fakefile, format='PNG')
            fakefile.seek(0)
            b64ver = base64.b64encode(fakefile.read())
            b64ver = b64ver.decode('utf-8')
            self.write("data:image/png;base64," + str(b64ver))



def main():
    tornado.options.parse_command_line()

    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }

    application = tornado.web.Application([
        (r'/(crossdomain\.xml)', tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static/")}),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static/")}),
        (r"/api/v1/sets", ImageSetsHandler),
        (r"/api/v1/bgsets", ImageBackgroundSetsHandler),
        (r"/(.*)", ImageHandler),
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port)

    print("The Oven is warmed up - Time to make some Robots! Listening on port: " + str(options.port))
    tornado.ioloop.IOLoop.instance().start()



if __name__ == "__main__":
        main()
