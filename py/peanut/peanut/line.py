import enum
from point import Point2D

class LineDrawer:
    class AlgoType(enum.Enum):
        NAIVE = enum.auto()
        DDA = enum.auto()
        BRESENHMAN = enum.auto()

    @staticmethod
    def naive_line_drawing_algorithm(x1, x2, y1, y2):
        dx = x2 - x1
        dy = y2 - y1
        pts = []
        for x in range(x1, x2, 1):
            y = y1 + dy * (x - x1) / dx
            pts.append(Point2D(x, y))
        return pts


    @staticmethod
    def digital_differential_analyzer(x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        if dx >= dy:
            step = dx
        else:
            step = dy

        dx /= step
        dy /= step
        x = x1
        y = y1
        i = 1
        pts = []
        while i < step:
            pts.append(Point2D(x, y))
            x += dx
            y += dy
            i += 1
        return pts

    @staticmethod
    def dda2(x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x = x1
        y = y1

        if dx > dy:
            steps = dx
        else: steps = dy

        xincr = dx / float(steps)
        yincr = dy / float(steps)
        pts = []
        pts.append(Point2D(round(x), round(y)))
        for _ in range(steps):
            x += xincr
            y += yincr
            pts.append(Point2D(round(x), round(y)))
        return pts

    @staticmethod
    def bresenhman_algorithm(x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        x = x1
        y = y1
        pts = []
        pts.append(Point2D(x, y))

        incrX = 2 * dy
        incrY = 2 * (dy - dx)
        pk = (2 * dy) - dx

        while x < x2:
            if pk < 0:
                x += 1
                pk += incrX
            else:
                x += 1
                y += 1
                pk += incrY
            pts.append(Point2D(x, y))
        return pts