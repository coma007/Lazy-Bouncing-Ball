import numpy as np
import utils.params as p
from objects.Vector import Vector


class Ball(object):
    """
    Klasa Ball koja modeluje Lea.
    """

    def __init__(self, diameter=20, mass=p.ball_mass, color=(27, 3, 163)):
        """
        Konstruktor klase Ball.

        :param diameter: polurecnik
        :type diameter: float
        :param mass: masa
        :type mass: float
        :param color: boja
        :type color: tuple
        """
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
        self._jumping = False
        self._moving = True

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
        if self._v_h == self._v_v == 0:
            return 0, 0
        if self._v_h == 0 and self._v_v != 0:
            return self._v_v, np.pi/2
        angle = np.arctan(self._v_v/self._v_h)
        intensity = np.sqrt(self._v_v**2 + self._v_h**2)
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
        angle = np.arctan(self._a_v/self._a_h)
        intensity = np.sqrt(self._a_v**2 + self._a_h**2)
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

    @y.setter
    def y(self, new_y):
        self._y = new_y

    @property
    def coor(self):
        return self._x, self._y

    @property
    def v_h_max(self):
        return self._v_h_max

    @property
    def I(self):
        return 2/5 * self._m * self._r ** 2

    @property
    def Q(self):
        return p.g * self._m

    @property
    def moving(self):
        return self._moving

    @moving.setter
    def moving(self, can_i_move):
        self._moving = can_i_move

    @property
    def jumping(self):
        return self._jumping

    @jumping.setter
    def jumping(self, do_i_jump):
        self._jumping = do_i_jump
        if do_i_jump:
            self._v_h += p.v_up * np.cos(p.angle_up)
            self._v_v += p.v_up * np.sin(p.angle_up)

    def do_gravity(self, terrain):
        for x, y in terrain:
            if x == self._x + self._r:
                self._y = y - self._r
                break


    # funkcije potrebne za detekciju kolizija

    # tacke sa najvecim i najmanjim koordinatama za sudare
    def get_max_coordinates(self):
        return [self._x + self._r, self._y + self._r]

    def get_min_coordinates(self):
        return [self._x - self._r, self._y - self._r]

    def furthest_point(self, vector):
        v = vector * self._r
        support_v = Vector(self._x + v.x, self._y + v.y)
        return support_v

    @property
    def center(self):
        return Vector(self._x, self._y)
