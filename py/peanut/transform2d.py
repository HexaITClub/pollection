import typing 
import math
import shape

class AffineTransform():
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
    def get_rotation(degree):
        return AffineTransform(matrix = [[math.cos(degree), -math.sin(degree), 0],
                                            [math.sin(degree), math.cos(degree), 0],
                                            [0, 0, 1]])

    @staticmethod
    def get_scaling(sx, sy):
        return AffineTransform(matrix = [[sx, 0, 0],
                                            [0, sy, 0],
                                            [0, 0, 1]])

    @property
    def matrix(self):
        return self.__transformation_matrix


if __name__ == "__main__":
    t = AffineTransform()