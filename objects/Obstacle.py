import utils.params as p
import numpy as np
from objects.Vector import Vector, dot


# hexagon
class Obstacle(object):
    """
    Klasa Obstacle koja modeluje prepreke na podlozi.
    """

    def __init__(self, x, number_of_sides=6, diameter=40, mass=1, color=(212, 123, 74)):
        """
        Konstruktor klase Obstacle.

        :param x: x koordinata centra prepreke
        :type x: float
        :param number_of_sides: broj strana prepreke
        :type number_of_sides: int
        :param diameter: poluprecnik opisanog kruga
        :type diameter: float
        :param mass: masa
        :type mass: float
        :param color: boja
        :type color: tuple
        """
        self._r = diameter
        self._m = mass
        self._v_h = 0  # horizontal velocity
        self._v_v = 0  # vertical velocity
        self._a_h = 0  # horizontal acceleration
        self._a_v = 0  # vertical acceleration
        self._color = color
        self._x = x  # x coordinate of position
        self._y = 410  # y coordinate of position
        self._number_of_sides = number_of_sides

    @property
    def m(self):
        return self._m

    @property
    def number_of_sides(self):
        return self._number_of_sides

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
        if self._a_v == self._a_h == 0:
            return 0, 0
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

    @property
    def coor(self):
        return self._x, self._y

    @property
    def I(self):
        return 2/5 * self._m * self._r ** 2

    @property
    def Q(self):
        return p.g * self._m

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
        vertices = self.get_all_vertices()
        furthest_point = None
        max_dist = np.NINF
        for vertex in vertices:
            point = Vector(vertex[0], vertex[1])
            dist = dot(point, vector)
            if dist > max_dist:
                furthest_point = point
                max_dist = dist
        return furthest_point

    @property
    def center(self):
        return Vector(self._x, self._y)

    # samo funkcija za testiranje, posle je obrisati
    @y.setter
    def y(self, value):
        self._y = value

    def get_all_vertices(self):
        vertices = [(self._x, self._y-self._r)]
        for i in range(self._number_of_sides-1):
            old_vertex = vertices[-1]
            new_vertex = ((old_vertex[0] - self._x)*np.cos((2 * np.pi)/self._number_of_sides) - (self._y - old_vertex[1])*np.sin((2 * np.pi)/self._number_of_sides) + self._x,
                          self._y - ((self._y - old_vertex[1])*np.cos((2 * np.pi)/self._number_of_sides) + (old_vertex[0] - self._x) * np.sin((2 * np.pi)/self._number_of_sides)))
            vertices.append(new_vertex)
        return vertices

    def get_position(self, ball):
        self._x -= ball.v_h

    def get_position_jump(self, ball):
        self._x -= ball.v_h / 10
