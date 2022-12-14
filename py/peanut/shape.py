from line import LineDrawer
from point import Point2D

class Shape2D:
    def __init__(self, points):
        self.__points = points

    def get_drawable(): pass

    @classmethod
    def from_points(cls, points):
        return cls(points)


class Line2D(Shape2D):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_drawable(self):
        return LineDrawer.digital_differential_analyzer(self.x1, self.y1, self.x2, self.y2)

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