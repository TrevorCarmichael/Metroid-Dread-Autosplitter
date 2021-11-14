import cv2
import numpy as np
import pytesseract
import variables
import config
from PIL import Image
from coordinates import Coordinates
from route import Route
from livesplit import LivesplitServer

cap = cv2.VideoCapture(config.cam_number)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  config.capture_frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.capture_frame_height)

ls = LivesplitServer(config.livesplit_server, config.livesplit_port)
ls.connect()

locations           = variables.locations
upgrades            = variables.upgrades
route               = variables.route
SCALE               = config.ACTUAL_WIDTH / 1920
item_coords         = Coordinates(410,410,1500,670,config.STARTING_X, config.STARTING_Y, SCALE)
location_coords     = Coordinates(656,40,1263,130,config.STARTING_X, config.STARTING_Y, SCALE)
decay_value         = 10
cooldown_length     = 200
route               = Route(variables.route)

def get_text_from_frame(frame, coord, thresh):
    crop   = cv2.cvtColor(frame[coord.y:coord.y+coord.h, coord.x:coord.x+coord.w], cv2.COLOR_BGR2GRAY)
    image  = Image.fromarray(crop).point(lambda p: p > thresh and 255)
    return pytesseract.image_to_string(image)

def main():

    item_cooldown       = 0
    location_cooldown   = 0
    current_location    = locations[0]

    print("Metroid Dread Autosplit")
    print("-----------------------")
    print("Press control+c at any time to abort the script.")
    print("Using scale %s" % SCALE)
    print("")
    print("Route:")
    route.print_route()
    print("-----------------------")
    print("")
    print("Starting Route watch...")
    print("First split is %s" % route.get_split_text(0))

    ret, frame = cap.read()

    print('Showing image from capture. If you don\'t see Metroid here then make sure that VirtualCam is started in OBS. If it is, try changing the cam_number variable until you see something here...')
    print('Green boxes show where we\'re watching for info. This should be roughly where the text when receiving an upgrade and taking transports appears. If it isn\'t right then check the X/Y/Width/Height values in config.')
    
    cv2.rectangle(frame, (item_coords.x, item_coords.y),(item_coords.x2, item_coords.y2),(0,255,0))
    cv2.rectangle(frame, (location_coords.x, location_coords.y),(location_coords.x2, location_coords.y2),(0,255,0))
    image = Image.fromarray(frame)
    image.show()

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Did not get frame from camera...")
            break
        
        if not route.is_complete():

            location_ocr    = get_text_from_frame(frame, location_coords,   config.threshold_value_locations)
            upgrade_ocr     = get_text_from_frame(frame, item_coords,       config.threshold_value_items)
            current_split   = route.get_current_split()

            if current_split[0] == "u":
                upg = upgrades[current_split[1]]
                
                if upg in upgrade_ocr:
                    print("%s split found at %s" % (upg, ls.get_current_time()))
                    ls.send_split()
                    route.progress_route()
                    route.print_current_split()
                    
            elif current_split[0] == "l":
                split_location_before   = current_split[1]
                split_location_after    = current_split[2]

            #good lord fix this 'if' salad
            if any(loc.upper() in location_ocr for loc in locations):
                for loc in locations:
                    if loc.upper() in location_ocr:
                        if loc != current_location and location_cooldown == 0:
                            if current_split[0] == "l":
                                if current_location == locations[split_location_before] and loc == locations[split_location_after]:
                                    print("%s to %s split found at %s" % (locations[split_location_before], locations[split_location_after], ls.get_current_time()))
                                    ls.send_split()
                                    route.progress_route()
                                    route.print_current_split()
                            else:
                                print("Detected location change from %s to %s." % (current_location, loc))

                            current_location  = loc
                            location_cooldown = cooldown_length
            
            if "Missile Tank" in upgrade_ocr and item_cooldown == 0:
                print("Collected Missile Tank in %s at %s" % (current_location,ls.get_current_time()))
                item_cooldown = cooldown_length
            elif "Missile+ Tank" in upgrade_ocr and item_cooldown == 0:
                print("Collected Missile+ Tank in %s at %s" % (current_location,ls.get_current_time()))
                item_cooldown = cooldown_length
            elif "Energy Tank" in upgrade_ocr and item_cooldown == 0:
                print("Collected Energy Tank in %s at %s" % (current_location,ls.get_current_time()))
                item_cooldown = cooldown_length

            item_cooldown       = item_cooldown     - decay_value if item_cooldown      > 0 else 0
            location_cooldown   = location_cooldown - decay_value if location_cooldown  > 0 else 0

main()