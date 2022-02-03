import numpy as np


class Vector(object):
    def __init__(self, x, y, z=0):
        if np.isnan(x):
            x = 0
        if np.isnan(y):
            y = 0
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def __str__(self):
        return "[" + str(self._x) + " , " + str(self._y) + " , " + str(self._z) + "]"

    # mnozenje vectora nekim skalarom
    def __mul__(self, other):
        return Vector(self._x * other, self._y * other)

    # oduzimanje dva vektora
    def __sub__(self, other):
        return Vector(self._x - other.x, self._y - other.y)

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y and self._z == other.z

    def set(self, x, y, z=0):
        if np.isnan(x):
            self._x = 0
        else:
            self._x = x
        if np.isnan(y):
            self._y = 0
        else:
            self._y = y
        if np.isnan(z):
            self._z = 0
        else:
            self._z = z

    def to_np_array(self):
        return np.array([self._x, self._y, self._z])


def dot(vector1, vector2):
    return vector1.x * vector2.x + vector1.y * vector2.y + vector1.z * vector2.z


def triple_product(vector1, vector2, vector3):
    vector1_array = vector1.to_np_array()
    vector2_array = vector2.to_np_array()
    vector3_array = vector3.to_np_array()
    support_vector_array = np.cross(vector1_array, vector2_array)
    triple_product_array = np.cross(vector3_array, support_vector_array)
    triple_product_vector = Vector(triple_product_array[0], triple_product_array[1])
    return triple_product_vector


def magnitude(vector):
    return np.sqrt(vector.x**2 + vector.y**2)

if __name__ == '__main__':
    vector1 = Vector(1, 2)
    vector2 = Vector(2, 7)
    vector3 = triple_product(vector1, vector2, vector1)
    print(vector3)
