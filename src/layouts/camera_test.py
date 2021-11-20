import PySimpleGUI as sg
import cv2
from PIL import Image, ImageTk
from auto_splitter.capture import Capture
from auto_splitter.variables import get_coordinates
from auto_splitter.coordinates import Coordinates

def window(x,y,w,h,c):
    
    camera_test = [[sg.Text('Cam Number'), sg.In(default_text=c, key="-CAM_NUM-",size=(2, 1), ), sg.Button('Update')],
                   [sg.Image(key='-IMAGE-', size=(1920/4, 1080/4))],
                   [sg.Button('Ok'), sg.Text('For best results do not obstruct the green boxes with stream elements!')]]

    window = sg.Window('Camera Configuration', camera_test)

    c = 0
    scale = w/1920
    l_coords, i_coords, menu_coords = get_coordinates(x, y, scale)
    all_triggers = [l_coords, i_coords, menu_coords[0], menu_coords[1], menu_coords[2],
            Coordinates(420, 420, 520, 650, x, y, scale),
            Coordinates(1390, 420, 1490, 650, x, y, scale),
            Coordinates(392, 462, 1533, 507, x, y, scale),
            Coordinates(392, 605, 1533, 650, x, y, scale),
            Coordinates(392, 749, 1533, 794, x, y, scale),
            Coordinates(0, 0, 1920, 1080, x, y, scale),
            Coordinates(50,50,550,250,x,y,scale),
            Coordinates(1370,50,1870,250,x,y,scale),
            Coordinates(1750, 920, 1780, 950, x, y, scale)
    ]

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Quit"):
            return c
            break

        if event == 'Update':
            c = int(values['-CAM_NUM-'])
            cap = Capture(c, 1920, 1080)
            ret, frame = cap.read()
            if ret:
                image = cap.draw_capture_zones(*all_triggers)
                image = image.resize((int(1920/4), int(1080/4)), resample=Image.BICUBIC)
                view_image = ImageTk.PhotoImage(image)
                window['-IMAGE-'].update(data=view_image)
                
            cap.close()

        if event == 'Ok':
            c = values['-CAM_NUM-']
            window.close()
            return c

    window.close()
    return c


