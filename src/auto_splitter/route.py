import auto_splitter.variables as variables
class Route:
    def __init__(self, route): 
        self.route = route
        self.route_pos = 0

    def get_current_split(self):
        if not self.is_complete():
            return self.route[self.route_pos]
        else: 
            return "Route complete"

    def progress_route(self):
        self.route_pos += 1

    def is_complete(self):
        return True if self.route_pos == len(self.route) else False

    def get_split_text(self, i):
        if i <= len(self.route):
            split = self.route[i]
            if split[0] == "u":
                return "%s" % variables.upgrades[split[1]]
            elif split[0] == "l":
                before = variables.locations[split[1]]
                after = variables.locations[split[2]]
                return "Transport from %s to %s" % (before, after)
        else:
            return "Autosplit is complete!"

    def print_current_split(self):
        if self.is_complete():
            return "Autosplit is complete!"
        else:
            return self.get_split_text(self.route_pos)

    def print_route(self):
        for i in range(0, len(self.route)):
            print(self.get_split_text(i))

    def set_route_position(self, i):
        if i < len(self.route) and i >= 0:
            self.route_pos = i
        elif i > len(self.route):
            self.route_pos = len(self.route)
        elif i <= 0: 
            self.route_pos = 0