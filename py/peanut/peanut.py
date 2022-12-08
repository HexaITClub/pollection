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
        pk = (2 * dy) - dx
        if x2 > x1:
            x = x1
            y = y1
            xend = x2
        else:
            x = x2
            y = y2
            xend = x1

        yield (x, y)

        while x < xend:
            x += 1
            if pk < 0:
                pk += (2 * dy)
            else:
                y += 1
                pk += (2 * dy) - (2 * dx)
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

        color = self.color
        while x >= y:
            self.pixels[(yc + y) * self.width + (xc + x)] = color
            self.pixels[(yc + x) * self.width + (xc + y)] = color
            self.pixels[(yc + x) * self.width - (xc + y)] = color
            self.pixels[(yc + y) * self.width - (xc + x)] = color
            self.pixels[(yc - y) * self.width - (xc + x)] = color
            self.pixels[(yc - x) * self.width - (xc + y)] = color
            self.pixels[(yc - x) * self.width + (xc + y)] = color
            self.pixels[(yc - y) * self.width + (xc + x)] = color
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
    canvas.color = 0xFFFFFF
    canvas.init_line_algorithm(LineDrawer.AlgoType.BRESENHMAN)
    canvas.draw_line(0, 0, 300, 40)
    ppm.save_as_ppm("output.ppm", canvas(), W, H)
