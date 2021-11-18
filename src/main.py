import PySimpleGUI as sg
import cv2
import ui_layouts
import layouts.camera as camera_layout
import layouts.livesplit as livesplit_layout
import layouts.route as route_layout
import layouts.calibrate as calibrate_layout
import json
import threading
from PIL import Image, ImageTk
from auto_splitter.livesplit import LivesplitServer
from auto_splitter.capture import Capture
from auto_splitter.coordinates import Coordinates
from auto_splitter.route import Route
import auto_splitter.variables as variables
from time import sleep

try: 
    with open('data.json', 'r') as f:
        config = json.load(f)
except:
    config = {
            "x": 0, 
            "y": 0,
            "w": 1920, 
            "h": 1080,
            "c": 0,
            "ls_server": "localhost",
            "ls_port": 16834,
            "route": [],
            "calib_1": [],
            "calib_2": [],
            "calib_3": []
        }


livesplit_server = config['ls_server']
livesplit_port = int(config['ls_port'])
x = int(config['x'])
y = int(config['y'])
w = int(config['w'])
h = int(config['h'])
c = int(config['c'])
calib_1 = config['calib_1']
calib_2 = config['calib_2']
calib_3 = config['calib_3']
scale = x/1920
route = config['route']
running = False
item_coords, location_coords, menu_coords = variables.get_coordinates(x,y,x/1920)

#sg.preview_all_look_and_feel_themes()
sg.theme('DarkPurple6')

column_2 = [[sg.Text("", key='-STAT1-')],
            [sg.Text("", key='-STAT2-')],
            [sg.Text("", key='-STAT3-')],
            [sg.Text("", key='-STAT4-')],
            [sg.Text("", key='-STAT5-')]]

column_1 = [[sg.Button('Route', key='-RTEBTN-'), sg.Text("No route selected", key="-ROUTETEXT-")],
               [sg.Button('Camera', key='-CAMBTN-'), sg.Text("No camera configured", key="-CAMTEXT-")],
               [sg.Button('Livesplit', key='-LSBTN-'), sg.Text("Livesplit not connected", key="-LSTEXT-")],
               [sg.Button('Test', key='-TSTBTN-'), sg.Button('Calibrate', key='-CALBTN-'), sg.Button('Save Config'), sg.Button('Start', key='-STARTBUTTON-')]]

main_layout = [[sg.Column(column_1), sg.Column(column_2)]]

window = sg.Window('Metroid Dread Autosplitter', main_layout, size=(500, 150))

def array_distance(arr1, arr2, num):
    if (arr1[0] < arr2[0] + num) and (arr1[0] > arr2[0] - num) and (arr1[1] < arr2[1] + num) and (arr1[1] > arr2[1] - num) and (arr1[2] < arr2[2] + num) and (arr1[2] > arr2[2] - num):
            return True
    else: 
        return False

def autosplit_thread(started=False):
    global running

    window['-STAT2-'].update('')
    window['-STAT3-'].update('')
    window['-STAT4-'].update('')
    window['-STAT5-'].update('')
    cap = Capture(c, 1920, 1080)

    ls = LivesplitServer(livesplit_server, livesplit_port)
    ls.connect()

    locations           = variables.locations
    upgrades            = variables.upgrades
    items               = variables.item_types

    SCALE = w/1920
    item_coords, location_coords, menu_coords = variables.get_coordinates(x,y,w/1920)
    
    decay_value = 10
    cooldown_length = 200

    item_cooldown = 0
    current_location = locations[0]
    item_count = 0
    averages = []

    final_route = Route(route)

    final_route.print_route()

    while not started and running:
        ret, frame = cap.read()
        if ret:
            averages = [
                cap.get_average_color_from_frame(frame, menu_coords[0]),
                cap.get_average_color_from_frame(frame, menu_coords[1]),
                cap.get_average_color_from_frame(frame, menu_coords[2])
            ]
            
            if array_distance(averages[1],calib_2,4) and array_distance(averages[2],calib_3,4):
                window['-STAT1-'].update('Detected file menu', text_color='green')
                if averages[0][0] > calib_1[0]+20:
                    started = True
                    ls.start_timer()
                    print("Started Timer!")
            else:
                window['-STAT1-'].update('Not on file menu', text_color='red')

    print("First split is %s" % final_route.get_split_text(0))

    window['-STAT1-'].update('Split watcher active!', text_color='green')
    window['-STAT2-'].update('Current Location: %s' % current_location, text_color='green')
    window['-STAT3-'].update('Items Collected: %s' % item_count, text_color='green')
    window['-STAT4-'].update('Next Split: %s' % final_route.print_current_split(), text_color='green')

    while started and running:
        ret, frame = cap.read()
        if ret: 
            if not final_route.is_complete():

                location_ocr    = cap.get_text_from_frame(frame, location_coords,   40)
                upgrade_ocr     = cap.get_text_from_frame(frame, item_coords,       120)
                current_split   = final_route.get_current_split()
                
                if (current_split[0] == "u" and upgrades[current_split[1]] in upgrade_ocr):
                    upg = upgrades[current_split[1]]
                    print("%s split found at %s" % (upg, ls.get_current_time()))
                    ls.send_split()
                    final_route.progress_route()
                    print(final_route.print_current_split())
                    window['-STAT4-'].update('Next Split: %s' % final_route.print_current_split(), text_color='green')

                elif current_split[0] == "l":
                    split_location_before   = current_split[1]
                    split_location_after    = current_split[2]
                
                for loc in locations:
                    if loc.upper() in location_ocr and loc != current_location:
                        if current_split[0] == "l" and current_location == locations[split_location_before] and loc == locations[split_location_after]:
                            print("%s to %s split found at %s" % (locations[split_location_before], locations[split_location_after], ls.get_current_time()))
                            ls.send_split()
                            final_route.progress_route()
                            print(final_route.print_current_split())
                            window['-STAT2-'].update('Current Location: %s' % loc, text_color='green')
                            window['-STAT4-'].update('Next Split: %s' % final_route.print_current_split(), text_color='green')
                            
                        else:
                            print("Detected location change from %s to %s at %s" % (current_location, loc, ls.get_current_time()))
                            window['-STAT2-'].update('Current Location: %s' % loc, text_color='green')
                        current_location  = loc
                        

                if item_cooldown == 0 and any(item in upgrade_ocr for item in items):
                    for item in items:
                        if item in upgrade_ocr:
                            print("Collected %s in %s at %s" % (item, current_location, ls.get_current_time()))
                            item_cooldown = cooldown_length
                            item_count += 1
                            window['-STAT3-'].update('Items Collected: %s' % item_count, text_color='green')

                item_cooldown = item_cooldown - decay_value if item_cooldown > 0 else 0

        if not ret: 
            print("No video from camera!")

    cap.close()

## UI LOOP BELOW
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == '-RTEBTN-':
        route = route_layout.window(route)
        print(route)

    if event == '-LSBTN-':
        livesplit_server, livesplit_port = livesplit_layout.window(livesplit_server, livesplit_port)
        print("Livesplit server set to %s:%s" % (livesplit_server, livesplit_port))
        window['-LSTEXT-'].update('Livesplit configured', text_color='green')

    if event == '-CAMBTN-':
        x, y, w, h, c = camera_layout.window(x,y,w,h,c)
        print("Video located at (%s, %s) with dimensions %s x %s" % (x,y,w,h))
        print("Using Camera %s" % c)
        window['-CAMTEXT-'].update('Camera configured', text_color='green')
    
    if event == 'Save Config':
        data = {
            "x": x, 
            "y": y,
            "w": w, 
            "h": h,
            "c": c,
            "ls_server": livesplit_server,
            "ls_port": livesplit_port,
            "route": route,
            "calib_1": calib_1,
            "calib_2": calib_2,
            "calib_3": calib_3
        }

        with open('data.json', 'w') as f:
            json.dump(data,f)

    if event == '-TSTBTN-':
        if len(route) > 0:
            window['-ROUTETEXT-'].update('Found route!', text_color='green')

        ls = LivesplitServer(livesplit_server, livesplit_port)

        if ls.valid_connection():
            window['-LSTEXT-'].update('Livesplit connected!', text_color='green')
        else: 
            window['-LSTEXT-'].update('Couldn\'t connect to Livesplit', text_color='red')
            
        cap = Capture(c, 1920, 1080)
        try:
            ret, frame = cap.read()
            if ret:
                window['-CAMTEXT-'].update('Camera connected!', text_color='green')
        except: 
                window['-CAMTEXT-'].update('Something went wrong!', text_color='red')

        cap.close()

    if event == '-STARTBUTTON-':
        if running == True:
            running = False
            window['-STARTBUTTON-'].update('Start')
            window['-STAT1-'].update('Stopped!', text_color='red')
            window['-STAT2-'].update('')
            window['-STAT3-'].update('')
            window['-STAT4-'].update('')
            window['-STAT5-'].update('')
            window['-CAMBTN-'].update(disabled=False)
            window['-RTEBTN-'].update(disabled=False)
            window['-LSBTN-'].update(disabled=False)
            window['-TSTBTN-'].update(disabled=False)
            window['-CALBTN-'].update(disabled=False)

        elif running == False:
            running = True
            window['-STARTBUTTON-'].update('Stop')
            threading.Thread(target=autosplit_thread, args=(), daemon=True).start()
            window['-CAMBTN-'].update(disabled=True)
            window['-RTEBTN-'].update(disabled=True)
            window['-LSBTN-'].update(disabled=True)
            window['-TSTBTN-'].update(disabled=True)
            window['-CALBTN-'].update(disabled=True)

    if event == '-CALBTN-':
        calib_1, calib_2, calib_3 = calibrate_layout.window(calib_1, calib_2, calib_3, x, y, w/1920, c)

window.close()