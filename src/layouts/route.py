import PySimpleGUI as sg
import auto_splitter.variables as variables
from time import sleep
import json
def read_routes_from_file():
    try: 
        with open('routes.json', 'r') as f:
            config = json.load(f)
    except:
        config = {
            'routes': [
                ['Default', []]
                ]
        }

    return config['routes']

def save_routes_to_file(routes):
    routes = {
        "routes": routes
    }

    with open('routes.json', 'w') as f:
            json.dump(routes,f)

def window(load_remove_only = False):
    get_names = lambda x: [i[0] for i in x]

    routes_list = read_routes_from_file()
    get_selected_index = lambda x: routes_list.index(x)
    route_names = get_names(routes_list) 

    selected_route_index = 0

    #print(routes_list)

    route = routes_list[0][1]
    route_text = []
    
    load_remove_only_mode = load_remove_only

    print(route)
    for i in route:
        if i[0] == "u":
            route_text.append(variables.upgrades[i[1]])
        elif i[0] == "l":
            route_text.append("%s to %s" % (variables.locations[i[1]], variables.locations[i[2]]))

    column_1 = [[sg.InputCombo(route_names, size=(16,1), key="-ROUTE_NAME-", default_value=route_names[0], readonly=True, enable_events=True)],
                [sg.T('Select an upgrade trigger:')],
                [sg.Listbox(values=variables.upgrades, key='-UPGRADES-', size=(20, 10), enable_events=True)],
                [sg.T('Before location -> Destination:')],
                [sg.Listbox(values=variables.locations, key='-LOCBEFORE-', size=(10, 10), no_scrollbar=True), sg.Listbox(values=variables.locations, key='-LOCAFTER-', enable_events=True, size=(10, 10), no_scrollbar=True)]]
    
    column_2 = [[sg.B('Add Upgrade Trigger')],
                [sg.B('Add Location Change Trigger')],
                [sg.B('Remove selected trigger')],
                [sg.Checkbox('Load Remover Only Mode', enable_events=True, default=load_remove_only_mode, key='-LOAD_REMOVER-')],
                [sg.B('Done'), sg.B('Save Route')]]

    column_3 = [[sg.B('↑')],
                [sg.B('↓')]]

    column_4 = [[sg.Text("Current Route")],
        [sg.Listbox(values=route_text, key='-ROUTE-', size=(40, 30))]]

    route_layout = [[sg.Column(column_1), sg.Column(column_2, element_justification='c'), sg.Column(column_3), sg.Column(column_4)]]

    window = sg.Window('Route Config', route_layout)

    

    while True: 
        event, values = window.read()

        if (event in (sg.WIN_CLOSED, "Quit")):
            return route, load_remove_only_mode
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
            selected = window['-ROUTE-'].GetIndexes()[0] if len(window['-ROUTE-'].GetIndexes()) > 0 else 0

            if len(route) > 0: 
                route_text.pop(selected)
                route.pop(selected)

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

        if event == "↑":
            selected = window['-ROUTE-'].GetIndexes()[0] if len(window['-ROUTE-'].GetIndexes()) > 0 else 0
            if selected > 0: 
                temp = route[selected-1]
                route[selected-1] = route[selected]
                route[selected] = temp

                route_text = []
                for i in route:
                    if i[0] == "u":
                        route_text.append(variables.upgrades[i[1]])
                    elif i[0] == "l":
                        route_text.append("%s to %s" % (variables.locations[i[1]], variables.locations[i[2]]))
                window['-ROUTE-'].update(values=route_text)
                window['-ROUTE-'].update(scroll_to_index=selected-1)
                window['-ROUTE-'].update(set_to_index=selected-1)

        if event == "↓":
            selected = window['-ROUTE-'].GetIndexes()[0] if len(window['-ROUTE-'].GetIndexes()) > 0 else len(route)

            if selected < len(route) - 1: 
                temp = route[selected+1]
                route[selected+1] = route[selected]
                route[selected] = temp

                route_text = []
                for i in route:
                    if i[0] == "u":
                        route_text.append(variables.upgrades[i[1]])
                    elif i[0] == "l":
                        route_text.append("%s to %s" % (variables.locations[i[1]], variables.locations[i[2]]))
                window['-ROUTE-'].update(values=route_text)
                window['-ROUTE-'].update(scroll_to_index=selected+1)
                window['-ROUTE-'].update(set_to_index=selected+1)

        if event == "Done":
            window.close()
            return route, load_remove_only_mode
        
        if event in ("-ROUTE_NAME-", "-ROUTE_COMBO-"):

            print(values['-ROUTE_NAME-'])
            selected_route_index = route_names.index(values['-ROUTE_NAME-'])

            route = routes_list[selected_route_index][1]

            route_text = []
            

            for i in route:
                if i[0] == "u":
                    route_text.append(variables.upgrades[i[1]])
                elif i[0] == "l":
                    route_text.append("%s to %s" % (variables.locations[i[1]], variables.locations[i[2]]))
            
            window['-ROUTE-'].update(values=route_text)

        if event == "-LOAD_REMOVER-":
            load_remove_only_mode = not load_remove_only_mode
            window['-LOAD_REMOVER-'].update(load_remove_only_mode)

        if event == "Save Route":
            event, values = sg.Window('Save Route',
                  [[sg.T('Enter name of route'), sg.In(key='-NAME-')],
                  [sg.B('OK')]]).read(close=True)

            route_name = values['-NAME-']
            print(route_name)

            routes_list.append([route_name, route])
            save_routes_to_file(routes_list)
            routes = read_routes_from_file()
            route_names = get_names(routes)
            print(route_names)
            window.Element('-ROUTE_NAME-').Update(values=route_names)

    window.close()
    return route, load_remove_only_mode