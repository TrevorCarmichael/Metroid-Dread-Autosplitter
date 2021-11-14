# Metroid Dread Autosplitter

A simple auto split program in Python. This uses OCR to read parts of the screen and determine when an upgrade or location change has happened.

At the moment I can only split on these actions. I've been trying to think of methods to split in other spots but that's tricky and this was easy. 

Please understand updates will be slow to this. I do work fulltime and like playing vidyagames so during the week I probably won't spend much time working on this. If you're someone who knows python then I'd recommend someone smarter than me forking this and making it better, or just make your own idk. I'm not a professional I'm just a dude who mildly understands how to program sometimes. This project was really just a 'proof of concept' I made that I guess might mature eventually. 

**Note this doesn't START or STOP the timer. It only splits. You'll need to start on continue like normal, and stop at the ending cutscene!** I don't intend on ever adding start/stop functionality at the moment. If the application messes up I'd like to not mess up someones time so manually starting and stopping I think is the best way to do that!

## How to use

1. First, we'll need TesseractOCR. You can install that from here: 
https://github.com/tesseract-ocr/tesseract/releases

Theoretically I think any version should work, but use 5.0.0. Just install to default location. 

2. Once this is installed, you'll also need this OBS plugin: 

https://obsproject.com/forum/resources/obs-virtualcam.949/

Install this to OBS. You can start it by going to Tools -> VirtualCam -> Start. This is needed because the default OBS camera doesn't seem to interface properly with the OCR software. Not sure if this is an OBS problem or a problem with the package I'm using

3. Make sure you have Python. https://www.python.org/downloads/. I built this using Python 3.9 but 3.10 should work just fine. 

4. Download this repository to some location. Put it somewhere doesn't matter where. 

5. In a console, CD to the directory you downloaded to into the 'src' directory. For me that would be 'cd F:\Projects\Autosplitter_Metroid_Dread\Metroid-Dread-Autosplitter\src'.

6. In the same command prompt run 'pip install .' to install the dependencies. 

7. Setup LiveSplit server (https://github.com/LiveSplit/LiveSplit.Server). This lets me send splits to livesplit. You'll need to add the 'LiveSplit Server' component to your layout in Livesplit, and then right click your splits and go to Control -> Start Server

8. Make sure Livesplit is running and the server is active, and OBS is running with VirtualCam on! These must be started Before the script.

9. Start the program with 'python main.py' from the scr directory. 

If this seems like a lot of work for an autosplitter that's because it is. This kind of started as a Friday project when I had some free time and I didn't originally make it for anyone else to use. Mostly a free time project that went too far. My goal is to strip down some of these steps and make it more friendly but for now this is what I have lol

The default route is for my Any% NMG route. An interface for setting up the route is also something I need to work on. 

## Configuring 

Open the config.py file to see the config settings. Most of these don't need to be touched, but the first 5 are pretty important. 

The first 4 settings get from your capture card in OBS. Right click the capture card and go to Transform -> Edit Transform. The 'Position' X and Y is the starting X and Y below. The 'Size' is the ACTUAL_WIDTH and ACTUAL_HEIGHT. This is needed so it's looking in the right spot and in case you aren't full screening the game in OBS. If OBS has the game fullscreened the defauls should be fine.

The cam_number you just need to play with... if 1 doesn't show an image, try 0. If that doesn't work try 2. Unfortunately the package I use to interface with the cam doesn't have a way to like, check the name of the cam. You just gotta play with it. 

STARTING_X                  = 0\
STARTING_Y                  = 0\
ACTUAL_WIDTH                = 1920\
ACTUAL_HEIGHT               = 1080\
cam_number                  = 1

## Setting the route

variables.py contains a 'route' array. This is what determines the order that the application is looking for split points. It only checks the next split to reduce load on the computer. 

A line starting with "u" is an upgrade. "l" is a location change. If we look at the first few lines here in mine: 

["u", 0], <-- This is getting the Charge Beam upgrade\
["u", 1], <-- This is getting the Phantom Cloak upgrade\
["u", 2], <-- This is getting the Spider Magnet upgrade\
["l", 0, 1], <-- This is changing locations from Artaria to Cataris\
["l", 1, 2], <-- This is changing locations from Cataris to Dairon\

The indexes here are in this order: 

0="Artaria"\
1="Cataris"\
2="Dairon"\
3="Burenia"\
4="Ghavoran"\
5="Ferenia"\
6="Elun"\
7="Hanubia"\
8="Itorash"

0="Charge Beam"\
1="Phantom Cloak"\
2="Spider Magnet"\
3="Wide Beam"\
4="Morph Ball"\
5="Varia Suit"\
6="Diffusion Beam"\
7="Grapple Beam"\
8="Bomb"\
9="Flash Shift"\
10="Speed Booster"\
11="Super Missile"\
12="Plasma Beam"\
13="Ice Missile"\
14="Space Jump"\
15="Screw Attack"\
16="Gravity Suit"\
17="Cross Bomb"\
18="Storm Missile"\
19="Wave Beam"\
20="Power Bomb"

## TODO

1. A GUI to set the route up. The current 'edit a file' is dumb and messy
2. A skip option for if the autosplitter fucks something up. Right now if it gets off sync you jsut gotta go back to LiveSplit manually. I'll add better syncing options between the two at some point. 
3. Fuzzy text searching. The OCR is pretty accurate like 99% of the time, but sometimes it will mis-interpret a character. I think using a text-distance to check if it's 95% similar would help these situations. Right now it's only exact matching. 
4. Reduce the amount of manual setup
5. lots of other stuff idk
