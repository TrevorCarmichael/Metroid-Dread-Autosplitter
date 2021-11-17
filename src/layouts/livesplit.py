import PySimpleGUI as sg

def window(server="localhost", port=16834):
    livesplit_layout = [[sg.In(default_text=server, size=(20, 1), key="-SERVER-"), sg.In(default_text=port, size=(5, 1), key="-PORT-")],
                [sg.Button('Ok')]]

    window = sg.Window('Livesplit Config', livesplit_layout)

    while True: 
        event, values = window.read()

        if (event in (sg.WIN_CLOSED, "Quit")):
            return server, port
            break

        if event == "Ok":
            window.close()
            return values['-SERVER-'], int(values['-PORT-'])

    window.close()
    return server, port