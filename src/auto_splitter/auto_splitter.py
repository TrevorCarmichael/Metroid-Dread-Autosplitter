import cv2
import time
import numpy                    as np 
from time                       import sleep
from PIL                        import Image
from auto_splitter.capture      import Capture
from auto_splitter.coordinates  import Coordinates
from auto_splitter.route        import Route
from auto_splitter.livesplit    import LivesplitServer
import auto_splitter.variables  as variables
import PySimpleGUI              as sg

class AutoSplitter():

    def __init__(self, x,y,w,h,c,window,route,livesplit_server, livesplit_port, load_remover_only=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c
        self.watching = False
        self.scale = w/1920
        self.trigger_distance = 10
        self.window = window
        self.route = route
        self.livesplit_server = livesplit_server
        self.livesplit_port = livesplit_port
        self.load_remover_only = load_remover_only

    def array_distance(self, arr1, arr2, num):
        if (arr1[0] < arr2[0] + num) and (arr1[0] > arr2[0] - num) and (arr1[1] < arr2[1] + num) and (arr1[1] > arr2[1] - num) and (arr1[2] < arr2[2] + num) and (arr1[2] > arr2[2] - num):
                return True
        else: 
            return False

    def lessthan(self, arr, num): 
        if arr[0] < num and arr[1] < num and arr[2] < num: 
            return True
        else: 
            return False

    def average_colors(self, frame, args):
        total = [0,0,0]
        for arg in args:
            arg_color = Capture.get_average_color_from_frame(frame, arg)
            total[0] += arg_color[0]
            total[1] += arg_color[1]
            total[2] += arg_color[2]
        return [int(total[0]/len(args)),int(total[1]/len(args)),int(total[2]/len(args))]

    def stop_watcher(self): 
        self.watching = False
        
    def start_watcher(self):
        self.watching = True

        x, y, w, h, c = self.x, self.y, self.w, self.h, self.c

        scale = w/1920
        item_coords, location_coords, menu_coords = variables.get_coordinates(x,y,w/1920)
        item_triggers = [
            Coordinates(420, 420, 520, 650, x, y, scale),
            Coordinates(1390, 420, 1490, 650, x, y, scale)
        ]

        item_trigger_value = [2, 12, 23]

        menu_triggers = [
            Coordinates(392, 462, 1533, 507, x, y, scale),
            Coordinates(392, 605, 1533, 650, x, y, scale),
            Coordinates(392, 749, 1533, 794, x, y, scale)
        ]

        menu_trigger_values = [[160, 46, 64], 
                               [31, 48, 56], 
                               [25, 41, 48]
        ]

        escape_sequence_trigger_value = [36, 1, 7]

        locations, upgrades, items = variables.locations, variables.upgrades, variables.item_types
        
        whole_screen_trigger = Coordinates(0, 0, 1920, 1080, x, y, scale)

        location_triggers = [
            Coordinates(50,50,550,250,x,y,scale),
            Coordinates(1370,50,1870,250,x,y,scale)
        ]

        loading_symbol = Coordinates(1750, 920, 1780, 950, x, y, scale)
        loading_symbol_trigger = [201, 255, 254]

        location_trigger_value = [0, 1, 8]

        last_time = time.time()

        cap = Capture(c, 1920, 1080)

        running = False
        
        ls = LivesplitServer(self.livesplit_server, self.livesplit_port, self.load_remover_only)
        ls.connect()

        route = Route(self.route) if not self.load_remover_only else Route([])
        current_location = locations[0]

        item_cooldown = 0
        upgrade_cooldown = 0
        item_count = 0
        split_location_before, split_location_after = 0, 0

        game_time_status = False
        timer_stage = 0

        death_screen_trigger = [39, 33, 43]

        end_frame_trigger = [55, 97, 127] #[55, 97, 127]
        end_frame_loc_trigger = [93, 165, 200] #[93, 165, 200]

        self.window['-STAT1-'].update('Current Location: %s' % "Artaria", text_color='green')
        self.window['-STAT2-'].update('Items Collected: %s' % item_count, text_color='green')
        self.window['-STAT3-'].update('Next Split: %s' % route.print_current_split())

        if self.load_remover_only:
            print("Starting in load remover only mode. Will not split! Will still start/stop GAME TIME in Livesplit.")

        print("Note: Game time in the first 10 seconds may appear wrong. It will reset before the initial load finishes!")
        watch_for_end_frame = False

        ls_index_sync_time = 0

        while self.watching:
            ret, frame = cap.read()

            if ret:
                avg = cap.get_average_color_from_frame(frame, whole_screen_trigger)
                #avg2 = cap.get_average_color_from_frame(frame, location_coords)
                #avg3 = cap.get_average_color_from_frame(frame, loading_symbol)
                
                #print("%s : %s : %s" % (avg, avg2, avg3))

                if not running: 
                    averages = [
                        cap.get_average_color_from_frame(frame, menu_triggers[0]),
                        cap.get_average_color_from_frame(frame, menu_triggers[1]),
                        cap.get_average_color_from_frame(frame, menu_triggers[2])
                    ]
                    if self.array_distance(averages[1], menu_trigger_values[1], self.trigger_distance) and self.array_distance(averages[2], menu_trigger_values[2], self.trigger_distance):
                        self.window['-STAT4-'].update('Detecting: File menu')
                        if averages[0][0] > menu_trigger_values[0][0] + 15:
                            print("Detected file start! Starting RTA timer...")
                            ls.start_timer()
                            running = True
                            game_time_status = False
                            timer_stage = 4
                            sleep(10)
                            ls.stop_game_timer()
                            ls.reset_game_time()
                            ret, frame = cap.read()

                else: 
                    screen_color = cap.get_average_color_from_frame(frame, whole_screen_trigger)
                    #print(screen_color)

                    if self.lessthan(screen_color, 10):
                        self.window['-STAT4-'].update('Detecting: Black Screen')
                        if timer_stage == 0:
                            loading_colors = cap.get_average_color_from_frame(frame, loading_symbol)
                            if self.array_distance(loading_colors, loading_symbol_trigger, 4):
                                timer_stage = 6
                        if timer_stage == 1: 
                            ls.stop_game_timer()
                            game_time_status = False
                            timer_stage = 2
                        elif timer_stage == 3: 
                            timer_stage = 4
                        elif timer_stage == 6:
                            ls.stop_game_timer()
                            game_time_status = False
                            timer_stage = 4
                    elif watch_for_end_frame and self.array_distance(screen_color, end_frame_trigger, 10):
                        end_frame_2 = cap.get_average_color_from_frame(frame, location_coords)
                        print(end_frame_2)
                        if self.array_distance(end_frame_2, end_frame_loc_trigger, 10):
                            print("Is this the end?")
                            ls.send_split()
                            self.stop_watcher()

                    else: 
                        current_split = route.get_current_split()
                        loc_colors = self.average_colors(frame, location_triggers)

                        if timer_stage == 2: 
                            timer_stage = 3
                        elif timer_stage == 4:
                            ls.start_game_timer()
                            game_time_status = True
                            timer_stage = 0

                        if current_split[0] == "l":
                            split_location_before   = current_split[1]
                            split_location_after    = current_split[2]

                        if self.array_distance(loc_colors, location_trigger_value, self.trigger_distance):
                            location_ocr = cap.get_text_from_frame(frame, location_coords, 40)
                            self.window['-STAT4-'].update('Detecting: Map Screen?')
                            current_split = route.get_current_split()
                            for loc in locations:
                                if loc.upper() in location_ocr and loc != current_location:
                                    if current_split[0] == "l" and current_location == locations[split_location_before] and loc == locations[split_location_after]:
                                        print("%s to %s split found at %s" % (locations[split_location_before], locations[split_location_after], ls.get_current_time()))
                                        ls.send_split()
                                        route.progress_route()
                                        self.window['-STAT3-'].update('Next Split: %s' % route.print_current_split(), text_color='green')
                                    
                                    timer_stage = 1
                                    current_location = loc
                                    self.window['-STAT1-'].update('Current Location: %s' % loc, text_color='green')
                                    if self.load_remover_only and loc == "Itorash":
                                        watch_for_end_frame = True

                        elif self.array_distance(loc_colors, death_screen_trigger, 4):
                            death_ocr = cap.get_text_from_frame(frame, item_coords, 80)
                            if "CONTINUE" in death_ocr:
                                timer_stage = 6
                        else: 
                            item_colors = self.average_colors(frame, item_triggers)
                            if self.array_distance(item_colors, item_trigger_value, self.trigger_distance):

                                self.window['-STAT4-'].update('Detecting: Upgrade/Item Window?')

                                upgrade_ocr = cap.get_text_from_frame(frame, item_coords, 120)

                                if current_split[0] == "u" and upgrades[current_split[1]] in upgrade_ocr:
                                    upg = upgrades[current_split[1]]
                                    print("%s split found at %s" % (upg, ls.get_current_time()))
                                    ls.send_split()
                                    route.progress_route()
                                    self.window['-STAT3-'].update('Next Split: %s' % route.print_current_split())

                                else:
                                    if item_cooldown <= 0:
                                        for item in items:
                                            if item in upgrade_ocr:
                                                print("Collected %s in %s at %s" % (item, current_location, ls.get_current_time()))
                                                item_cooldown = 10
                                                item_count += 1
                                                self.window['-STAT2-'].update('Items Collected: %s' % item_count, text_color='green')
                                    if upgrade_cooldown <= 0:
                                        for upg in upgrades:
                                            if upg in upgrade_ocr:
                                                print("Found %s at %s" % (upg, ls.get_current_time()))
                                                upgrade_cooldown = 10


                            else: 
                                self.window['-STAT4-'].update('Game playing...')
                            
                        self.window['-STAT6-'].update('Route Complete: %s, Timer_stage: %s' % (route.is_complete(), timer_stage))

                        #TIMEKEEPING LOGIC BELOW
                        end_time = time.time()
                        diff =  (end_time - last_time)

                        #Sync with Livesplit index every 10 seconds
                        if not self.load_remover_only:
                            ls_index_sync_time += diff
                            if ls_index_sync_time > 10: 
                                ls_index = ls.get_current_index()
                                if ls_index != route.route_pos:
                                    print("Skipping to split %s" % route.get_split_text(ls_index))
                                    route.set_route_position(ls_index)
                                ls_index_sync_time = 0

                        #Once an item/upgrade is collected, don't check for 10 more seconds
                        #Prevents duplicate readings....
                        if item_cooldown > 0:
                            item_cooldown -=  diff
                        if upgrade_cooldown > 0:
                            upgrade_cooldown -= diff

                        self.window['-STAT5-'].update('Processing %s FPS' % round(1 / diff))
                        last_time = end_time