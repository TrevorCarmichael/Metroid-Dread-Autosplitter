import io
import PySimpleGUI as sg
import cv2
from PIL import Image
from auto_splitter.capture import Capture
from auto_splitter.variables import get_coordinates
from auto_splitter.coordinates import Coordinates

def list_ports():
    current_port = 0
    is_working = True
    working_ports = []
    available_ports = []
    names = []
    print([cv2.videoio_registry.getBackendName(b) for b in cv2.videoio_registry.getCameraBackends()])

    while is_working:
        cam = cv2.VideoCapture(current_port)

        if not cam.isOpened():
            is_working = False
        else:
            ret, frame = cam.read()

            if ret: 
                print("Port %s (%s) is reading." % (current_port,cam.getBackendName()))
                available_ports.append(current_port)
                names.append("%s (%s)" % (current_port, cam.getBackendName()))
            else: 
                print("Port %s is connected, but not reading..." % current_port)
            current_port += 1

    return available_ports, names

def window(x=0, y=0, w=1920, h=1080, c=0):

    x2 = x + w
    y2 = y + h
    avail_cameras, names = list_ports()
    camera_test = [[sg.Text('Cam Number'), sg.InputCombo(avail_cameras, size=(4,1), key="-CAM_NUM-"), sg.Button('Update'), sg.Text('If this appears blurry, don\'t worry too much. The actual rendering when running will be upped to 1080.')],
                   [sg.Image(key='-IMAGE-', size=(1920/2, 1080/2))],
                   [sg.Button('Ok'), sg.Text('X'),sg.In(default_text=x, size=(5, 1), key="-X-"), sg.Text('Y'), sg.In(default_text=y, size=(5, 1), key="-Y-"),sg.Text('Width'),sg.In(default_text=x2, size=(5, 1), key="-W-"),sg.Text('Height'),sg.In(default_text=y2, size=(5, 1), key="-H-"),sg.Text('For best results do not obstruct the green boxes with stream elements!')]]

    window = sg.Window('Camera Configuration', camera_test)

    scale = w/1920

    l_coords, i_coords, menu_coords = get_coordinates(x, y, scale)

    all_triggers = [l_coords, i_coords, menu_coords[0], menu_coords[1], menu_coords[2],
            Coordinates(420, 420, 620, 650, x, y, scale),
            Coordinates(1290, 420, 1490, 650, x, y, scale),
            Coordinates(392, 462, 1533, 507, x, y, scale),
            Coordinates(392, 605, 1533, 650, x, y, scale),
            Coordinates(392, 749, 1533, 794, x, y, scale),
            Coordinates(0, 0, 1919, 1079, x, y, scale),
            Coordinates(50,50,550,250,x,y,scale),
            Coordinates(1370,50,1870,250,x,y,scale),
            Coordinates(1750, 920, 1780, 950, x, y, scale)
    ]
    cap = None
    print(avail_cameras)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Quit"):
            return x, y, w, h, c
            break

        if event == 'Update':
            if c != int(values['-CAM_NUM-']) or cap is None:
                c = int(values['-CAM_NUM-'])
                print("Init cam %s" %c)
                cap = Capture(c)

            x, y, w, h = int(values['-X-']),int(values['-Y-']),int(values['-W-']),int(values['-H-'])
            scale = w/1920

            l_coords, i_coords, menu_coords = get_coordinates(x, y, scale)

            all_triggers = [l_coords, i_coords, menu_coords[0], menu_coords[1], menu_coords[2],
                    Coordinates(420, 420, 620, 650, x, y, scale),
                    Coordinates(1290, 420, 1490, 650, x, y, scale),
                    Coordinates(392, 462, 1533, 507, x, y, scale),
                    Coordinates(392, 605, 1533, 650, x, y, scale),
                    Coordinates(392, 749, 1533, 794, x, y, scale),
                    Coordinates(0, 0, 1919, 1079, x, y, scale),
                    Coordinates(50,50,550,250,x,y,scale),
                    Coordinates(1370,50,1870,250,x,y,scale),
                    Coordinates(1750, 920, 1780, 950, x, y, scale)
            ]
            print("Trying Device %s at %s x %s" % (c, cap.get_width(), cap.get_height()))
            ret, frame = cap.read()
            if ret:
                image = Capture.draw_capture_zones_on_frame(frame, *all_triggers)
                image = image.resize((int(1920/2), int(1080/2)), resample=Image.BICUBIC)
                view_image = io.BytesIO()
                image.save(view_image, format="PNG")
                window['-IMAGE-'].update(data=view_image.getvalue())

        if event == 'Ok':
            c = values['-CAM_NUM-']
            window.close()
            return x, y, w, h, c

    window.close()
    return x, y, w, h, c


