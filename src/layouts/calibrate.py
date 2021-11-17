import PySimpleGUI as sg
from auto_splitter.capture import Capture
import auto_splitter.variables as variables
from auto_splitter.coordinates import Coordinates

def window(calib_1 = [], calib_2 = [], calib_3 = [], x = 0, y = 0, scale = 1, c=0):
    _, _, menu_coords = variables.get_coordinates(x,y,scale)
    cap = Capture(c, 1920, 1080)
    calibrate_layout = [[sg.Text('After making sure camera configuration works, navigate to a')],
                        [sg.Text('file menu and hover on \'Continue\'. Then press the button below.')],
                        [sg.Button('Calibrate')]]

    window = sg.Window('Color Calibration', calibrate_layout)

    while True: 
        event, values = window.read()

        if (event in (sg.WIN_CLOSED, "Quit")):
            cap.close()
            return calib_1, calib_2, calib_3
            break

        if event == "Calibrate":
            ret, frame = cap.read()
            if ret:
                calib_1 = cap.get_average_color_from_frame(frame, menu_coords[0])
                calib_2 = cap.get_average_color_from_frame(frame, menu_coords[1])
                calib_3 = cap.get_average_color_from_frame(frame, menu_coords[2])
                window.close()
                cap.close()
                return calib_1, calib_2, calib_3

    window.close()
    cap.close()
    return calib_1, calib_2, calib_3