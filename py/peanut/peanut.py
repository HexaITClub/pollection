#!/usr/bin/env python3

import ppm
from line import LineDrawer
from shape import Circle2D, Line2D, Shape2D, Path2D
from transform2d import AffineTransform
import point

class PeanutCanvas:
    line_algo_type = LineDrawer.AlgoType.DDA

    def __init__(self, width, height, pixels = None):
        self.width = width
        self.height = height
        self.pixels = pixels if pixels else [0 for _ in range(height * width)]
        self._color = 0x0
        self.shapes_info = []
        self.transform = None


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


    def draw_circle(self, xc, yc, radius):
        circle = Circle2D(xc, yc, radius)
        self.shapes_info.append({"color": self.color, "shape": circle})

    def draw_line(self, x1, y1, x2, y2):
        line = Line2D(x1, y1, x2, y2)
        self.shapes_info.append({"color": self.color, "shape": line})
        
    def draw(self, shape: Shape2D):
        self.shapes_info.append({"color": self.color, "shape": shape})
    
    def __draw_all(self):
        for si in self.shapes_info:
            shape: Shape2D = si.get("shape")
            color: int = si.get("color")
            self.__transform_and_draw(shape, color)
    
    def __transform_and_draw(self, shape, color):
        if self.transform:
            if isinstance(shape, Line2D):
                start = point.Point2D(shape.x1, shape.y1)
                end = point.Point2D(shape.x2, shape.y2)
                self.transform.transform([start, end])
                shape.x1 = start.x
                shape.y1 = start.y
                shape.x2 = end.x
                shape.y2 = end.y
            elif isinstance(shape, Circle2D):
                center = point.Point2D(shape.centerx, shape.centery)
                self.transform.transform([center])
                shape.centerx = center.x
                shape.centery = center.y
        
        if isinstance(shape, Path2D):
            for path_obj in shape._shapes:
                self.__transform_and_draw(path_obj, color)
            return

        points = shape.get_drawable()
        for p in points:
            x = p.x
            y = p.y
            self.pixels[int(y) * self.width + int(x)] = color


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

    
    def set_transform(self, transform: AffineTransform):
        self.transform = transform


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
        self.__draw_all()
        return self.pixels


if __name__ == "__main__":
    W = 900
    H = 900
    
    canvas = PeanutCanvas(W, H)
    canvas.fill(0xFFFFFF)
    canvas.color = 0xFF0000
    canvas.draw_line(200, 200, 300, 300)
    canvas.draw_line(300, 300, 100, 300)
    canvas.draw_line(100, 300, 200, 200)
    ppm.save_as_ppm("out.ppm", canvas(), W, H)