from line import LineDrawer
from point import Point2D

class Shape2D:
    def __init__(self, points):
        self.__points = points

    def get_drawable(self): pass

    @classmethod
    def from_points(cls, points):
        return cls(points)


class Line2D(Shape2D):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.__line_type = LineDrawer.LineType.NORMAL

    def set_line_type(self, line_type: LineDrawer.LineType) -> None:
        self.__line_type = line_type

    def get_drawable(self):
        LineDrawer.__selected_line_type = self.__line_type
        pts = LineDrawer.dda2(self.x1, self.y1, self.x2, self.y2)
        LineDrawer.__selected_line_type = LineDrawer.LineType.NORMAL
        return pts

class Circle2D(Shape2D):
    def __init__(self, cx, cy, radius):
        self.centerx = cx
        self.centery = cy
        self.radius = radius

    def get_drawable(self):
        x = self.radius
        y = 0
        error = 0
        points = []
        while x >= y:
            pts = self.__gen_8_way_symmetry(x, y)
            for (px, py) in pts:
                points.append(Point2D((self.centerx + px), (self.centery + py)))
            if error <= 0:
                y += 1
                error += (2 * y) + 1
            elif error > 0:
                x -= 1
                error -= (2 * x) + 1
        return points
    
    def __gen_8_way_symmetry(self, x, y):
        return self.__gen_4_way_symmetry(x, y) + [
                    (y, -x),
                    (y, x),
                    (-y, x),
                    (-y, -x)
                ]

    def __gen_4_way_symmetry(self, x, y):
        return [
                (x, y),
                (-x, y),
                (x, -y),
                (-x, -y)
            ]

class Path2D(Shape2D):
    def __init__(self):
        self.__currentx = 0
        self.__currenty = 0
        self._shapes = []

    def move_to(self, x, y):
        self.__currentx = x
        self.__currenty = y

    def line_to(self, x, y):
        self._shapes.append(Line2D(self.__currentx, self.__currenty, x, y))
        self.__currentx = x
        self.__currenty = y

    def curve_to(self, x1, y1, x2, y2, x3, y3):
        raise Exception("Not implemented!")

    def transform(self, tf):
        raise Exception("Not implemented!")

    def get_drawable(self):
        draws = []
        for sh in self._shapes:
            draws += sh.get_drawable()
        return draws
