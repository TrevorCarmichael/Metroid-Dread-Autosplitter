class Coordinates:
        def __init__(self, x, y, x2, y2, offset_x, offset_y, scale):
            self.x = int((x  * scale) + offset_x)
            self.y = int((y  * scale) + offset_y)
            self.x2 = int((x2  * scale) + offset_x)
            self.y2 = int((y2  * scale) + offset_y)
            self.w = int((x2 * scale) + offset_x - self.x)
            self.h = int((y2 * scale) + offset_y - self.y)