import typing 
import math
import shape
import enum

class AffineTransform():
    class RotationDirection(enum.Enum):
        CLOCKWISE = enum.auto()
        COUNTER_CLOCKWISE = enum.auto()

    def __init__(self, matrix = None):
        self.__transformation_matrix = matrix

    def concatenate(self, affine_transform):
        if self.__transformation_matrix is None:
            self.__transformation_matrix = affine_transform.__transformation_matrix
        else: 
            self.__transformation_matrix = self.multiply_matrices(self.__transformation_matrix, affine_transform.matrix)

    def transform(self, points: typing.List[shape.Point2D]):
        if self.__transformation_matrix:
            for point in points:
                pt_matrix = [[point.x], [point.y], [1]]
                result = self.multiply_matrices(self.__transformation_matrix, pt_matrix)
                point.x = result[0][0]
                point.y = result[1][0]
        return points

    def multiply_matrices(self, m1, m2):
        m1_m = len(m1)
        m1_n = len(m1[0])
        m2_m = len(m2)
        m2_n = len(m2[0])
        if m1_n != m2_m: return None
        result = [[0 for _ in range(m2_n)] for _ in range(m1_m)]
        for i in range(m1_m):
            for j in range(m2_n):
                for k in range(m2_m):
                    result[i][j] += m1[i][k] * m2[k][j]
        return result

    @staticmethod
    def get_translation(tx, ty):
        return AffineTransform(matrix = [[1, 0, tx], 
                                            [0, 1, ty],
                                            [0, 0, 1]])

    @staticmethod
    def get_rotation(degree, direction: RotationDirection):
        if direction == AffineTransform.RotationDirection.CLOCKWISE:
            a12 = -math.sin(degree)
            a21 = math.sin(degree)
        elif direction == AffineTransform.RotationDirection.COUNTER_CLOCKWISE:
            a12 = math.sin(degree)
            a21 = -math.sin(degree)
        return AffineTransform(matrix = [[math.cos(degree), a12, 0],
                                            [a21, math.cos(degree), 0],
                                            [0, 0, 1]])

    @staticmethod
    def get_scaling(sx, sy):
        return AffineTransform(matrix = [[sx, 0, 0],
                                            [0, sy, 0],
                                            [0, 0, 1]])

    @staticmethod
    def get_reflection(rx, ry):
        return AffineTransform(matrix = [[rx, 0, 0],
                                            [0, ry, 0],
                                            [0, 0, 1]])

    @staticmethod
    def get_shearing(shx, shy):
        return AffineTransform(matrix = [[shx, 0, 0],
                                            [0, shy, 0],
                                            [0, 0, 1]])

    @property
    def matrix(self):
        return self.__transformation_matrix


import ppm
import shape
import peanut
import math

if __name__ == "__main__":
    t = AffineTransform(matrix=[[3, -math.cos(45), 5], [math.sin(90), 6, 7], [12, 34, 7]])
    ln = shape.Line2D(10, 10, 200, 200)
    pts = t.transform(ln.get_drawable())
    cv = peanut.PeanutCanvas(1000, 1000)
    cv.fill(0xFFFFFF)
    cv.color = 0xFF0000
    cv.draw(ln)
    ppm.save_as_ppm("./out.ppm", cv(), 1000, 1000)