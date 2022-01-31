import math


class Ball(object):

    def __init__(self, diameter=20, mass=2, color=(27, 3, 163)):
        self._r = diameter
        self._m = mass
        self._v_h = 0   # horizontal velocity
        self._v_v = 0   # vertical velocity
        self._a_h = 0   # horizontal acceleration
        self._a_v = 0   # vertical acceleration
        self._color = color
        self._x = 200   # x coordinate of position
        self._y = 0     # y coordinate of position
        self._v_h_max = 10

    @property
    def m(self):
        return self._m

    @property
    def r(self):
        return self._r

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
        angle = math.atan(self._v_v/self._v_h)
        intensity = math.sqrt(self._v_v**2 + self._v_h**2)
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
        angle = math.atan(self._a_v/self._a_h)
        intensity = math.sqrt(self._a_v**2 + self._a_h**2)
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

    def do_gravity(self, terrain):
        for x, y in terrain:
            if x == self._x + self._r:
                self._y = y - self._r
                break