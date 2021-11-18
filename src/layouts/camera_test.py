import PySimpleGUI as sg
import cv2
from PIL import Image, ImageTk
from auto_splitter.capture import Capture
from auto_splitter.variables import get_coordinates
from auto_splitter.coordinates import Coordinates

def window(x,y,w,h,c):
    
    camera_test = [[sg.Text('Cam Number'), sg.In(default_text=c, key="-CAM_NUM-",size=(2, 1), ), sg.Button('Update')],
                   [sg.Image(key='-IMAGE-', size=(1920/4, 1080/4))],
                   [sg.Button('Ok')]]

    window = sg.Window('Camera Configuration', camera_test)

    c = 0
    l_coords, i_coords, menu_coords = get_coordinates(x, y, w/1920)

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
                image = cap.draw_capture_zones(l_coords, i_coords, menu_coords[0], menu_coords[1], menu_coords[2])
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


