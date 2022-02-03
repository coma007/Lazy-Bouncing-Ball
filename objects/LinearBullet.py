import utils.params as p
import numpy as np


class LinearBullet(object):
    def __init__(self, x, length=10, mass=1, color=(0, 0, 0)):
        self._m = mass
        self._v_h = 0  # horizontal velocity
        self._v_v = 0  # vertical velocity
        self._a_h = 0  # horizontal acceleration
        self._a_v = 0  # vertical acceleration
        self._color = color
        self._x = x  # x coordinate of middle point
        self._y = 390  # y coordinate of all positions
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
        if self._v_v == self._v_h == 0:
            return 0, 0
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
        if self._a_v == self._a_h == 0:
            return 0, 0
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

    # skroz leva tacka
    def get_min_coordinates(self):
        return self._x - self._length, self._y

    # skroz desna tacka
    def get_max_coordinates(self):
        return self._x + self._length, self._y