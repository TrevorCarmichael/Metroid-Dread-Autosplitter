import PySimpleGUI as sg
import layouts.camera_test as camera_test_layout

def window(x=0, y=0, w=1920, h=1080, c=0):
    
    camera_layout = [[sg.Text('X'),sg.In(default_text=x, size=(5, 1), key="-X-")],
                    [sg.Text('Y'),sg.In(default_text=y, size=(5, 1), key="-Y-")],
                    [sg.Text('Width'),sg.In(default_text=w, size=(5, 1), key="-W-")],
                    [sg.Text('Height'),sg.In(default_text=h, size=(5, 1), key="-H-")],
                    [sg.Text('Get these from Livesplit. Right click source -> Transform -> Edit Transform')],
                    [sg.Text('\'Position\' will be your X and Y values. ')],
                    [sg.Text('\'Size\' will be your Width and Height values. ')],
                    [sg.Button('Set Cam Number'), sg.Button('Ok')]]

    window = sg.Window('Camera Configuration', camera_layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Quit"):
            return 0, 0, 1920, 1080, 0
            break

        if event == 'Set Cam Number':
            x, y, w, h = int(values['-X-']), int(values['-Y-']), int(values['-W-']), int(values['-H-'])
            c = int(camera_test_layout.window(x,y,w,h,c))

        if event == 'Ok':
            x, y, w, h = int(values['-X-']), int(values['-Y-']), int(values['-W-']), int(values['-H-'])
            window.close()
            return x, y, w, h, c

    window.close()
    return 0, 0, 1920, 1080, 0


