import PySimpleGUI as sg
import cv2
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
from auto_splitter.auto_splitter import AutoSplitter
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
            "load_remover_only": False
        }


livesplit_server = config['ls_server']
livesplit_port = int(config['ls_port'])
x = int(config['x'])
y = int(config['y'])
w = int(config['w'])
h = int(config['h'])
c = int(config['c'])
load_remover_only = config['load_remover_only']

scale = x/1920
route = config['route']

#sg.preview_all_look_and_feel_themes()
sg.theme('DarkPurple6')

column_2 = [[sg.Text("", key='-STAT1-')],
            [sg.Text("", key='-STAT2-')],
            [sg.Text("", key='-STAT3-')],
            [sg.Text("", key='-STAT4-')],
            [sg.Text("", key='-STAT5-')],
            [sg.Text("", key='-STAT6-')]]

column_1 = [[sg.Button('Route', key='-RTEBTN-'), sg.Text("No route selected", key="-ROUTETEXT-")],
               [sg.Button('Camera', key='-CAMBTN-'), sg.Text("No camera configured", key="-CAMTEXT-")],
               [sg.Button('Livesplit', key='-LSBTN-'), sg.Text("Livesplit not connected", key="-LSTEXT-")],
               [sg.Button('Test', key='-TSTBTN-'), sg.Button('Calibrate', key='-CALBTN-', disabled=False), sg.Button('Save Config'), sg.Button('Start', key='-STARTBUTTON-')]]

main_layout = [[sg.Column(column_1), sg.Column(column_2)]]

window = sg.Window('Metroid Dread Autosplitter', main_layout, size=(650, 180))
auto_splitter = AutoSplitter(x, y, w, h, c, window, route, livesplit_server, livesplit_port)

## UI LOOP BELOW
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == '-RTEBTN-':
        route, load_remover_only = route_layout.window(route, load_remover_only)
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
            "load_remover_only": load_remover_only
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
        

        if auto_splitter.watching == False:
            window['-STARTBUTTON-'].update('Stop')
            auto_splitter = AutoSplitter(x, y, w, h, c, window, route, livesplit_server, livesplit_port, load_remover_only)
            threading.Thread(target=auto_splitter.start_watcher, args=(), daemon=True).start()
            window['-CAMBTN-'].update(disabled=True)
            window['-RTEBTN-'].update(disabled=True)
            window['-LSBTN-'].update(disabled=True)
            window['-TSTBTN-'].update(disabled=True)
            #window['-CALBTN-'].update(disabled=True)
        elif auto_splitter.watching == True:
            auto_splitter.stop_watcher()
            sleep(1)
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
            #window['-CALBTN-'].update(disabled=False)

    if event == '-CALBTN-':
        calib_1, calib_2, calib_3 = calibrate_layout.window(calib_1, calib_2, calib_3, x, y, w/1920, c)

window.close()