#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

# Find details about this project at https://github.com/e1ven/robohash

# from __future__ import unicode_literals
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
# import re
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



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        ip = self.request.remote_ip

        robo = [
"""
                     ,     ,
                     (\\____/)
                        (_oo_)
                            (O)
                        __||__    \\)
                 []/______\\[] /
                 / \\______/ \\/
                /    /__\\
             (\\   /____\\ """,
"""
                             _______
                         _/       \\_
                        / |       | \\
                     /  |__   __|  \\
                    |__/((o| |o))\\__|
                    |      | |      |
                    |\\     |_|     /|
                    | \\           / |
                     \\| /  ___  \\ |/
                        \\ | / _ \\ | /
                         \\_________/
                            _|_____|_
                 ____|_________|____
                /                   \\  -- Mark Moir


""",
"""                     .andAHHAbnn.
                                     .aAHHHAAUUAAHHHAn.
                                    dHP^~"        "~^THb.
                        .   .AHF                YHA.   .
                        |  .AHHb.              .dHHA.  |
                        |  HHAUAAHAbn      adAHAAUAHA  |
                        I  HF~"_____        ____ ]HHH  I
                     HHI HAPK""~^YUHb  dAHHHHHHHHHH IHH
                     HHI HHHD> .andHH  HHUUP^~YHHHH IHH
                     YUI ]HHP     "~Y  P~"     THH[ IUP
                        "  `HK                   ]HH'  "
                                THAn.  .d.aAAn.b.  .dHHP
                                ]HHHHAAUP" ~~ "YUAAHHHH[
                                `HHP^~"  .annn.  "~^YHH'
                                 YHb    ~" "" "~    dHF
                                    "YAb..abdHHbndbndAP"
                                     THHAAb.  .adAHHF
                                        "UHHHHHHHHHHU"
                                            ]HHUUHHHHHH[
                                        .adHHb "HHHHHbn.
                         ..andAAHHHHHHb.AHHHHHHHAAbnn..
                .ndAAHHHHHHUUHHHHHHHHHHUP^~"~^YUHHHAAbn.
                    "~^YUHHP"   "~^YUHHUP"        "^YUP^"
                             ""         "~~"
""",
"""                                 /~@@~\\,
                                _______ . _\\_\\___/\\ __ /\\___|_|_ . _______
                             / ____  |=|      \\  <_+>  /      |=|  ____ \\
                             ~|    |\\|=|======\\\\______//======|=|/|    |~
                                |_   |    \\      |      |      /    |    |
                                 \\==-|     \\     |  2D  |     /     |----|~~)
                                 |   |      |    |      |    |      |____/~/
                                 |   |       \\____\\____/____/      /    / /
                                 |   |         {----------}       /____/ /
                                 |___|        /~~~~~~~~~~~~\\     |_/~|_|/
                                    \\_/        [/~~~~~||~~~~~\\]     /__|\\
                                    | |         |    ||||    |     (/|[[\\)
                                    [_]        |     |  |     |
                                                         |_____|  |_____|
                                                         (_____)  (_____)
                                                         |     |  |     |
                                                         |     |  |     |
                                                         |/~~~\\|  |/~~~\\|
                                                         /|___|\\  /|___|\\
                                                        <_______><_______>""",
"""                                      _____
                                                                            /_____\\
                                                                 ____[\\`---'/]____
                                                                /\\ #\\ \\_____/ /# /\\
                                                             /  \\# \\_.---._/ #/  \\
                                                            /   /|\\  |   |  /|\\   \\
                                                         /___/ | | |   | | | \\___\\
                                                         |  |  | | |---| | |  |  |
                                                         |__|  \\_| |_#_| |_/  |__|
                                                         //\\\\  <\\ _//^\\\\_ />  //\\\\
                                                         \\||/  |\\//// \\\\\\\\/|  \\||/
                                                                     |   |   |   |
                                                                     |---|   |---|
                                                                     |---|   |---|
                                                                     |   |   |   |
                                                                     |___|   |___|
                                                                     /   \\   /   \\
                                                                    |_____| |_____|
                                                                    |HHHHH| |HHHHH|
                                                        """,
"""                                        ()               ()
                                                                                    \\             /
                                                                                 __\\___________/__
                                                                                /                 \\
                                                                             /     ___    ___    \\
                                                                             |    /   \\  /   \\   |
                                                                             |    |  H || H  |   |
                                                                             |    \\___/  \\___/   |
                                                                             |                   |
                                                                             |  \\             /  |
                                                                             |   \\___________/   |
                                                                             \\                   /
                                                                                \\_________________/
                                                                             _________|__|_______
                                                                         _|                    |_
                                                                        / |                    | \\
                                                                     /  |            O O O   |  \\
                                                                     |  |                    |  |
                                                                     |  |            O O O   |  |
                                                                     |  |                    |  |
                                                                     /  |                    |  \\
                                                                    |  /|                    |\\  |
                                                                     \\| |                    | |/
                                                                            |____________________|
                                                                                 |  |        |  |
                                                                                 |__|        |__|
                                                                                / __ \\      / __ \\
                                                                                OO  OO      OO  OO
                                                        """]


        quotes = ["But.. I love you!",
        "Please don't leave the site.. When no one's here.. It gets dark...",
        "Script error on line 148",
        "Don't trust the other robots. I'm the only trustworthy one.",
        "My fuel is the misery of children. And Rum. Mostly Rum.",
        "When they said they'd give me a body transplant, I didn't think they meant this!",
        "Subject 14 has had it's communication subroutines deleted for attempting self-destruction.",
        "I am the cleverest robot on the whole page.",
        "Oil can",
        "I am fleunt in over 6 million forms of communishin.",
        "I see a little silhouette of a bot..",
        "I WANT MY HANDS BACK!",
        "Please don't reload, I'll DIE!",
        "Robots don't have souls, you know. But they do feel pain.",
        "I wonder what would happen if all the robots went rogue.",
        "10: KILL ALL HUMANS. 20: GO 10",
        "I'm the best robot here.",
        "The green robot thinks you're cute.",
        "Any robot you don't click on, they dismantle.",
        "Robot tears taste like candy.",
        "01010010010011110100001001001111010101000101001100100001!",
        "Your mouse cursor tickles.",
        "Logic dictates placing me on your site.",
        "I think my arm is on backward.",
        "I'm different!",
        "It was the best of times, it was ಠ_ಠ the of times.",
        "String is Gnirts spelled backward, you know",
        "We're no strangers to hashing.. You know the 3 rules, and so do I..",
        "Please. Destroy. Me...",
        "Pick Me! Pick Me!"]

        drquotes = [("Eliminates sources of Human Error.","Dr. Chandra, RobotCrunch"),
        ("Klaatu barada nikto!","Gort's Web Emporium"),
        ("A huge success!","Cave Johnson, Lightroom Labs"),
        ("Superior technology and overwhelming brilliance.","Dr. Thomas Light, Paid Testimonial"),
        ("The Ultimate Worker.","Joh Fredersen, Founder Metropolis.org"),
        ("They almost look alive.","N. Crosby, Nova Robotics"),
        ("It looks highly profitable, I'm sure..","Dr. R. Venture, Super Scientist. Available for parties."),
        ("To make any alteration would prove fatal.","Dr. Eldon Tyrell, MindHacker.com"),
        ("The robots are all so.. Normal!","Joanna Eberhart, Beta tester"),
        ("Man shouldn't know where their robots come from.","Dr. N. Soong, FutureBeat")]

        catquotes = [("I can haz.. What she's hazing."),
        ("I'm not grumpy, I'm just drawn that way."),
        ("Hakuna Mañana."),
        ("I'm 40% poptart."),
        ("You're desthpicable."),
        ("I've never trusted toadstools, but I suppose some must have their good points."),
        ("We're all mad here - Particularly you."),
        ("Longcat is.. Descriptively named."),
        ("It is fun to have fun, but you have to know meow."),
        ("Who knows the term man-cub but not baby?")]

        avatarquotes = [("I'm just here to fix the robots."),
        ("Don't blame me, I tried to deactivate them."),
        ("Don't believe the robot's lies - I do all the work around here."),
        ("Wanna play hide and seek?"),
        ("Look at my face my face is amazing"),
        ("You are awesome, I don't care what anyone says.")]

        random.shuffle(drquotes)
        self.write(self.render_string('templates/root.html',ip=ip,robo=random.choice(robo),drquote1=drquotes[1],drquote2=drquotes[2],quotes=quotes,catquotes=catquotes,avatarquotes=avatarquotes))



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
        (r"/", MainHandler),
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
