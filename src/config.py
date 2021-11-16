'''
In OBS, right click Capture card, select 'Transform' -> 'Edit Transform'. Get the values from there.
Position in the Edit Transform window will be the STARTING_X and STARTING_Y values
ACTUAL_WIDTH and ACTUAL_HEIGHT will be your 'size' values. This lets me calculate where the text will be no matter what size
your output is. Note that the smaller this is the 'worse' quality the OCR will be. Bigger is better. 
If your output is bigger than 1080p i honestly don't know if it will work i didn't test that lol
'''

STARTING_X                  = 0
STARTING_Y                  = 0
ACTUAL_WIDTH                = 1920
ACTUAL_HEIGHT               = 1080
cam_number                  = 0 #You may need to fiddle with this. Usually will be 0 or 1. 

#Probably don't change these
threshold_value_items       = 120 # 120 seems to work in almost every case I've found
threshold_value_locations   = 50  # I like 30 for this, lower bitrate vids might need higher

#This is the default and probably doesn't need to be changed.
livesplit_server = "localhost"
livesplit_port = 16834

#idk don't touch this lol
capture_frame_width  = 1920
capture_frame_height = 1080

debug = False
debug_path = "F:/Projects/Autosplitter_Metroid_Dread/Metroid-Dread-Autosplitter/src/debug_images"