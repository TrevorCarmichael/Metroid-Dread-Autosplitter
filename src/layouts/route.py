import PySimpleGUI as sg
import auto_splitter.variables as variables

def window(existing_route):
    route = existing_route if len(existing_route) > 0 else []
    route_text = []
    
    for i in existing_route:
        if i[0] == "u":
            route_text.append(variables.upgrades[i[1]])
        elif i[0] == "l":
            route_text.append("%s to %s" % (variables.locations[i[1]], variables.locations[i[2]]))

    column_1 = [[sg.Text('Select an upgrade trigger:')],
                [sg.Listbox(values=variables.upgrades, key='-UPGRADES-', size=(20, 10), enable_events=True)],
                [sg.Text('Before location -> Destination:')],
                [sg.Listbox(values=variables.locations, key='-LOCBEFORE-', size=(10, 10), no_scrollbar=True), sg.Listbox(values=variables.locations, key='-LOCAFTER-', enable_events=True, size=(10, 10), no_scrollbar=True)]]
    
    column_2 = [[sg.Button('Add Upgrade Trigger')],
                [sg.Button('Add Location Change Trigger')],
                [sg.Button('Remove selected trigger')],
                [sg.Button('Done')]]

    column_3 = [[sg.Text("Current Route")],
        [sg.Listbox(values=route_text, key='-ROUTE-', size=(40, 20))]]

    route_layout = [[sg.Column(column_1), sg.Column(column_2, element_justification='c'), sg.Column(column_3)]]

    window = sg.Window('Route Config', route_layout)

    

    while True: 
        event, values = window.read()

        if (event in (sg.WIN_CLOSED, "Quit")):
            return route
            break

        if event == "Add Upgrade Trigger":
            if len(values['-UPGRADES-']) > 0: 
                selection = values['-UPGRADES-'][0]
                if (selection is not None) and (selection in variables.upgrades) and (["u", variables.upgrades.index(selection)] not in route):
                    upg_index = variables.upgrades.index(selection)
                    route.append(["u", upg_index])
                    route_text.append(selection)
                    window['-ROUTE-'].update(values=route_text)

        if event == "Remove selected trigger":
            if len(values['-ROUTE-']) > 0: 
                selection = values['-ROUTE-'][0]
                route_index = route_text.index(selection)
                route_text.pop(route_index)
                route.pop(route_index)
                window['-ROUTE-'].update(values=route_text)

        if event == "Add Location Change Trigger":
            if len(values['-LOCBEFORE-']) > 0 and len(values['-LOCAFTER-']) > 0:
                before = values['-LOCBEFORE-'][0]
                after = values['-LOCAFTER-'][0]
                before_index = variables.locations.index(before)
                after_index = variables.locations.index(after)
                route.append(["l", before_index, after_index])
                route_text.append("%s to %s" % (before, after))
                window['-ROUTE-'].update(values=route_text)

        if event == "Done":
            window.close()
            return route

    window.close()
    return route