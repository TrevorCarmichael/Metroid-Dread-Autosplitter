import numpy as np
import variables
import config
from time import sleep
from PIL import Image
from coordinates import Coordinates
from route import Route
from livesplit import LivesplitServer
from capture import Capture

cap = Capture(config.cam_number, config.capture_frame_width, config.capture_frame_height)

ls = LivesplitServer(config.livesplit_server, config.livesplit_port)
ls.connect()

locations           = variables.locations
upgrades            = variables.upgrades
items               = variables.item_types
route               = variables.route
SCALE               = config.ACTUAL_WIDTH / 1920
item_coords         = Coordinates(410,410,1500,670,config.STARTING_X, config.STARTING_Y, SCALE)
location_coords     = Coordinates(656,40,1263,130,config.STARTING_X, config.STARTING_Y, SCALE)
menu_coords = [
    Coordinates(392, 462, 1533, 507, config.STARTING_X, config.STARTING_Y, SCALE),
    Coordinates(392, 605, 1533, 650, config.STARTING_X, config.STARTING_Y, SCALE),
    Coordinates(392, 749, 1533, 794, config.STARTING_X, config.STARTING_Y, SCALE)]
decay_value         = 10
cooldown_length     = 200
route               = Route(variables.route)
debug               = config.debug

menu_1 = []
menu_2 = []
menu_3 = []

def array_distance(arr1, arr2, num):
    if (arr1[0] < arr2[0] + num) and (arr1[0] > arr2[0] - num) and (arr1[1] < arr2[1] + num) and (arr1[1] > arr2[1] - num) and (arr1[2] < arr2[2] + num) and (arr1[2] > arr2[2] - num):
            return True
    else: 
        return False
def main():

    item_cooldown = 0
    current_location = locations[0]
    item_count = 0
    started = False
    averages = []

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
    print('Showing image from capture. If you don\'t see Metroid here then make sure that VirtualCam is started in OBS. If it is, try changing the cam_number variable until you see something here...')
    print('Green boxes show where we\'re watching for info. This should be roughly where the text when receiving an upgrade and taking transports appears. If it isn\'t right then check the X/Y/Width/Height values in config.')

    image = cap.draw_capture_zones(item_coords, location_coords)
    image.show()

    if debug: cap.save_frame("Startup")

    user_input = input("Start timer automatically? (Y/N) \nIf not automatic, start LiveSplit like normal.")

    if user_input == 'Y':
        user_input = input("Get game to the game file and hover over continue, then press Enter to calibrate.")
        ret, frame = cap.read()
        menu_1 = cap.get_average_color_from_frame(frame, menu_coords[0])
        menu_2 = cap.get_average_color_from_frame(frame, menu_coords[1])
        menu_3 = cap.get_average_color_from_frame(frame, menu_coords[2])
        print(menu_2)
        print(menu_3)

    while not started:
        ret, frame = cap.read()
        averages = [
            cap.get_average_color_from_frame(frame, menu_coords[0]),
            cap.get_average_color_from_frame(frame, menu_coords[1]),
            cap.get_average_color_from_frame(frame, menu_coords[2])
        ]
        print(averages)
        if array_distance(averages[1],menu_2,2) and array_distance(averages[2],menu_3,2) and averages[0][0] > menu_1[0]+30:
            started = True
            ls.start_timer()
            print("Started Timer!")

    while started:
    
        ret, frame = cap.read()

        if not ret:
            print("Did not get frame from camera...")
            break
        
        if not route.is_complete():

            location_ocr    = cap.get_text_from_frame(frame, location_coords,   config.threshold_value_locations)
            upgrade_ocr     = cap.get_text_from_frame(frame, item_coords,       config.threshold_value_items)
            current_split   = route.get_current_split()

            if (current_split[0] == "u" and upgrades[current_split[1]] in upgrade_ocr):
                upg = upgrades[current_split[1]]
                print("%s split found at %s" % (upg, ls.get_current_time()))
                if debug: save_frame(frame, upg)
                ls.send_split()
                route.progress_route()
                route.print_current_split()
                    
            elif current_split[0] == "l":
                split_location_before   = current_split[1]
                split_location_after    = current_split[2]

            for loc in locations:
                if loc.upper() in location_ocr and loc != current_location:
                    if current_split[0] == "l" and current_location == locations[split_location_before] and loc == locations[split_location_after]:
                        print("%s to %s split found at %s" % (locations[split_location_before], locations[split_location_after], ls.get_current_time()))
                        ls.send_split()
                        route.progress_route()
                        route.print_current_split()
                        if debug: save_frame(frame, "%s to %s" % (locations[split_location_before], locations[split_location_after]))
                    else:
                        print("Detected location change from %s to %s at %s" % (current_location, loc, ls.get_current_time()))
                        if debug: save_frame(frame, "%s to %s" % (current_location, loc))

                    current_location  = loc

            if item_cooldown == 0 and any(item in upgrade_ocr for item in items):
                for item in items:
                    if item in upgrade_ocr:
                        print("Collected %s in %s at %s" % (item, current_location, ls.get_current_time()))
                        item_cooldown = cooldown_length
                        if debug: save_frame(frame, "%s_%s_%s" % (item, current_location, item_count))
                        item_count += 1

            item_cooldown = item_cooldown - decay_value if item_cooldown > 0 else 0
main()