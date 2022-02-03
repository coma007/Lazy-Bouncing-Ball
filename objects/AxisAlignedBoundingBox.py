
class Interval(object):
    # ako je axis 0 - x osa
    # ako je axis 1 - y osa
    def __init__(self, aabb, axis=0):
        if axis == 0:
            self.start = aabb.min_point.x
            self.end = aabb.max_point.x
        else:
            self.start = aabb.min_point.y
            self.end = aabb.max_point.y
        self.object = aabb
        self._open = False

    def open(self):
        self._open = True

    def close(self):
        self._open = False

    def is_open(self):
        return self._open


class Point(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

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

    def __str__(self):
        return "[" + str(self._x) + " , " + str(self._y) + "]"

    def __sub__(self, other):
        return [self.x - other.x, self.y - other.y]


class AxisAlignedBoundingBox(object):
    def __init__(self, shape):
        self._shape = shape

        # svaki objekat mora imati funkcije koje vracaju minimalnu i maksimalnu tacku tog objekta
        min_coordinates = shape.get_min_coordinates()
        self._min_point = Point(min_coordinates[0], min_coordinates[1])
        max_coordinates = shape.get_max_coordinates()
        self._max_point = Point(max_coordinates[0], max_coordinates[1])

    def __str__(self):
        return "AABB: {min point: " + str(self._min_point) + "; max point: " + str(self._max_point) + "}"

    @property
    def shape(self):
        return self._shape

    @property
    def min_point(self):
        return self._min_point

    @min_point.setter
    def min_point(self, value):
        self._min_point.x = value.x
        self._min_point.y = value.y

    @property
    def max_point(self):
        return self._max_point

    @max_point.setter
    def max_point(self, value):
        self._max_point.x = value.x
        self._max_point.y = value.y

    def overlap_check(self, other):
        # minimalna tacka drugog aabb mora imati sve manje koordinate da bi se sekao sa ovim aabb
        dx = other.min_point.x - self._max_point.x
        dy = other.min_point.y - self._max_point.y
        if dx > 0 or dy > 0:
            return False

        # kontra smer
        dx = self._min_point.x - other.max_point.x
        dy = self._min_point.y - other.max_point.y

        if dx > 0 or dy > 0:
            return False

        return True

