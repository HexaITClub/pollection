#!/usr/bin/env python3

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

    def set_transform(self, transform: AffineTransform):
        self.transform = transform

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        self._color = c

    def __call__(self):
        self.__draw_all()
        return self.pixels

    def boundary_fill(self, x: int, y: int, fill_color: int, boundary_color: int) -> None:
        if ((x < 0) or (x >= self.width)) or ((y < 0) or (y >= self.height)): return
        index: int = y * self.width + x
        current_color = self.pixels[index]
        if (current_color != fill_color) and (current_color != boundary_color):
            self.pixels[index] = fill_color
            self.boundary_fill(x + 1, y, fill_color, boundary_color)
            self.boundary_fill(x - 1, y, fill_color, boundary_color)
            self.boundary_fill(x, y + 1, fill_color, boundary_color)
            self.boundary_fill(x, y - 1, fill_color, boundary_color)

    def flood_fill(self, x: int, y: int, fill_color: int, replace_color: int):
        pass