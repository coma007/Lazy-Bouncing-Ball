import utils.params as p
import numpy as np
from objects.Vector import Vector, dot


class LinearBullet(object):
    """
    Klasa LinearBullet koja modeluje metke.
    """

    def __init__(self, x, length=10, mass=1, color=(0, 0, 0)):
        """
        Konstruktor klase LinearBullet.

        :param x: x koordinata centra metka
        :type x: float
        :param length: duzina metka
        :type length: float
        :param mass: masa metka
        :type mass: float
        :param color: boja metka
        :type color: tuple
        """
        self._m = mass
        self._v_h = 10  # horizontal velocity
        self._v_v = 0  # vertical velocity
        self._a_h = 0  # horizontal acceleration
        self._a_v = 0  # vertical acceleration
        self._color = color
        self._x = x  # x coordinate of middle point
        self._y = 385  # y coordinate of all positions
        self._length = length
        self._v_h_max = 10

    @property
    def length(self):
        return self._length

    @property
    def m(self):
        return self._m

    @property
    def v_h(self):
        return self._v_h

    @v_h.setter
    def v_h(self, new_v):
        self._v_h = new_v

    @property
    def v_v(self):
        return self._v_v

    @v_v.setter
    def v_v(self, new_v):
        self._v_v = new_v

    @property
    def v(self):
        if self._v_h == self._v_v == 0:
            return 0, 0
        if self._v_h == 0 and self._v_v != 0:
            return self._v_v, np.pi/2
        angle = np.arctan(self._v_v / self._v_h)
        intensity = np.sqrt(self._v_v ** 2 + self._v_h ** 2)
        return intensity, angle

    @property
    def a_h(self):
        return self._a_h

    @a_h.setter
    def a_h(self, new_a):
        self._a_h = new_a

    @property
    def a_v(self):
        return self._a_v

    @a_v.setter
    def a_v(self, new_v):
        self._a_v = new_v

    @property
    def a(self):
        if self._a_h == self._a_v == 0:
            return 0, 0
        if self._a_h == 0 and self._a_v != 0:
            return self._a_v, np.pi/2
        angle = np.arctan(self._a_v / self._a_h)
        intensity = np.sqrt(self._a_v ** 2 + self._a_h ** 2)
        return intensity, angle

    @property
    def color(self):
        return self._color

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, new_x):
        self._x = new_x

    @property
    def coor(self):
        return self._x, self._y

    @property
    def v_h_max(self):
        return self._v_h_max

    @property
    def Q(self):
        return p.g * self._m

    @property
    def center(self):
        return Vector(self._x, self._y)

    # skroz leva tacka
    def get_min_coordinates(self):
        return self._x - self._length, self._y

    # skroz desna tacka
    def get_max_coordinates(self):
        return self._x + self._length, self._y

    def get_position(self, ball):
        self._x -= self.v_h + ball.v_h / 2

    def get_position_jump(self, ball):
        self._x -= self._v_h / 10 + ball.v_h / 500

    def furthest_point(self, vector):
        vertices = [self.get_min_coordinates(), self.get_max_coordinates()]
        furthest_point = None
        max_dist = np.NINF
        for vertex in vertices:
            point = Vector(vertex[0], vertex[1])
            dist = dot(point, vector)
            if dist > max_dist:
                furthest_point = point
                max_dist = dist
        return furthest_point
