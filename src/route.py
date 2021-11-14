import variables
class Route:
    def __init__(self, route): 
        self.route = route
        self.route_pos = 0

    def get_current_split(self):
        return self.route[self.route_pos]

    def progress_route(self):
        self.route_pos += 1

    def is_complete(self):
        return True if self.route_pos == len(self.route) else False

    def get_split_text(self, i):
        split = self.route[i]
        if split[0] == "u":
            return variables.upgrades[split[1]]
        elif split[0] == "l":
            before = variables.locations[split[1]]
            after = variables.locations[split[2]]
            return "Transport from %s to %s" % (before, after)

    def print_current_split(self):
        if self.is_complete():
            print("Autosplit is complete!")
        else:
            print(self.get_split_text(self.route_pos))

    def print_route(self):
        for i in range(0, len(self.route)):
            print(self.get_split_text(i))