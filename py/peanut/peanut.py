#!/usr/bin/env python3

import ppm
import enum
import image

class LineDrawer:
    class AlgoType(enum.Enum):
        NAIVE = enum.auto()
        DDA = enum.auto()
        BRESENHMAN = enum.auto()

    @staticmethod
    def naive_line_drawing_algorithm(x1, x2, y1, y2):
        dx = x2 - x1
        dy = y2 - y1
        for x in range(x1, x2, 1):
            y = y1 + dy * (x - x1) / dx
            yield (x, y)


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
        while i < step:
            yield (x, y)
            x += dx
            y += dy
            i += 1


    @staticmethod
    def bresenhman_algorithm(x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        x = x1
        y = y1
        yield (x, y)

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
            yield (x, y)


class PeanutCanvas:
    line_algo_type = LineDrawer.AlgoType.DDA

    def __init__(self, width, height, pixels = None):
        self.width = width
        self.height = height
        self.pixels = pixels if pixels else [0 for _ in range(height * width)]
        self._color = 0x0


    @classmethod
    def init_line_algorithm(cls, algo: LineDrawer.AlgoType) -> None:
        cls.line_algo_type = algo


    def draw_rect(self, x, y, width, height):
        self.draw_line(x, y, x + width, y)
        self.draw_line(x, y, x, y + height)
        self.draw_line(x, y + height, x + width, y + height)
        self.draw_line(x + width, y, x + width, y + height)


    def fill_rect(self, x, y, width, height):
        for dy in range(y, y + height):
            if dy >= 0 or dy < height:
                for dx in range(x, x + width):
                    if dx >= 0 or dx < width:
                        self.pixels[dy * self.width + dx] = self.color


    def fill(self, color):
        self.color = color
        self.fill_rect(0, 0, self.width, self.height)


    # mid point circle drawing algorithm
    def draw_circle(self, xc, yc, radius):
        x = radius
        y = 0
        error = 0
        while x >= y:
            pts = self.__gen_8_way_symmetry(x, y)
            for (px, py) in pts:
                self.pixels[(yc + py) * self.width + (xc + px)] = self.color
            if error <= 0:
                y += 1
                error += (2 * y) + 1
            elif error > 0:
                x -= 1
                error -= (2 * x) + 1


    def draw_line(self, x1, y1, x2, y2):
        if PeanutCanvas.line_algo_type == LineDrawer.AlgoType.NAIVE:
            line_pixel_coord_generator = LineDrawer.naive_line_drawing_algorithm(x1, y1, x2, y2)
        elif PeanutCanvas.line_algo_type == LineDrawer.AlgoType.DDA:
            line_pixel_coord_generator = LineDrawer.digital_differential_analyzer(x1, y1, x2, y2)
        elif PeanutCanvas.line_algo_type == LineDrawer.AlgoType.BRESENHMAN:
            self.__handle_bresenhman_line_algo(x1, y1, x2, y2)
            return

        for pixel_coord in line_pixel_coord_generator:
            x = pixel_coord[0]
            y = pixel_coord[1]
            self.pixels[int(y) * self.width + int(x)] = self.color


    def __handle_bresenhman_line_algo(self, x1, y1, x2, y2):
        line_pixel_coord_generator = LineDrawer.bresenhman_algorithm(x1, y1, x2, y2)
        for pixel_coord in line_pixel_coord_generator:
            x = pixel_coord[0]
            y = pixel_coord[1]
            self.pixels[y * self.width + x] = self.color

    
    def draw_polygon(self, xs, ys):
        length = len(xs)
        if length < 2:
            return

        i = 0
        while i < (length - 1):
            x1 = xs[i]
            y1 = ys[i]
            x2 = xs[i + 1]
            y2 = ys[i + 1]
            self.draw_line(x1, y1, x2, y2)
            i += 1

        x1 = xs[0]
        y1 = ys[0]
        x2 = xs[length - 1]
        y2 = ys[length - 1]
        self.draw_line(x1, y1, x2, y2)


    def draw_ellipse(self, cx, cy, a, b):
        x = 0
        y = b
        pts = self.__gen_4_way_symmetry(x, y)
        for (px, py) in pts:
            self.pixels[(cy + py) * self.width + (cx + px)] = self.color

        d1 = (b*b) - (a*a*b) + (0.25*a*a)
        while ((a*a)*(y-0.5)) > ((b*b)*(x+1)):
            if d1 < 0:
                d1 += (b*b) * (2*x + 3)
            else:
                d1 += ((b*b)*(2*x+3)) + ((a*a)*(-2*y+2))
                y -= 1
            x += 1

            pts = self.__gen_4_way_symmetry(x, y)
            for (px, py) in pts:
                self.pixels[(cy + py) * self.width + (cx + px)] = self.color

        d2 = ((b*b)*(x + 0.5)*(x + 0.5)) + ((a*a)*(y - 1)*(y - 1) - (a*a)*(b*a))
        while y > 0:
            if d2 < 0:
                d2 += ((b*b)*(2*x + 2)) + ((a*a)*(-2*y+3))
                x += 1
            else:
                d2 += (a*a)*(-2*y + 3)
            y -= 1

            pts = self.__gen_4_way_symmetry(x, y)
            for (px, py) in pts:
                self.pixels[(cy + py) * self.width + (cx + px)] = self.color


    def __gen_4_way_symmetry(self, x, y):
        return [
                (x, y),
                (-x, y),
                (x, -y),
                (-x, -y)
            ]

    def __gen_8_way_symmetry(self, x, y):
        return self.__gen_4_way_symmetry(x, y) + [
                    (y, -x),
                    (y, x),
                    (-y, x),
                    (-y, -x)
                ]


    @property
    def color(self):
        return self._color


    @color.setter
    def color(self, c):
        self._color = c


    def __call__(self):
        return self.pixels


if __name__ == "__main__":
    ROWS = 8
    COLS = 8
    W = 400
    H = 400
    
    canvas = PeanutCanvas(W, H)
    canvas.fill(0xFFFFFF)
    canvas.color = 0x000000
    canvas.draw_ellipse(200, 200, 50, 60)
    ppm.save_as_ppm("out.ppm", canvas(), W, H)
