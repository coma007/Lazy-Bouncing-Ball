import pygame

from objects.AxisAlignedBoundingBox import Interval, AxisAlignedBoundingBox
import numpy as np
from utils.physics import *

from objects.Bomb import Bomb
from objects.Obstacle import Obstacle
from objects.Vector import Vector, dot, triple_product, magnitude
from objects.LinearBullet import LinearBullet
from objects.Ball import Ball

ORIGIN = Vector(0, 0)


def sort_intervals(interval_list):
    """
    Funkcija sortira intervale svakog objekta.
    :param interval_list: Lista intervala.
    :type interval_list: list[objects.AxisAlignedBoundingBox.Interval]
    """
    j = 0
    while j != len(interval_list) - 1:
        for i in range(len(interval_list) - 1 - j):
            if interval_list[i].start > interval_list[i + 1].start:
                interval_list[i], interval_list[i + 1] = interval_list[i + 1], interval_list[i]
        j += 1
    return interval_list


# algoritam za deljenje prostora, kako ne bismo morali da proveravamo da li je doslo do sudara izmedju bilo koja dva
# objekta, nego samo izmedju nekih
# svaki aabb projektujemo na x osu, ako se intervali nekih aabb-a seku i oni se potencijalno seku
def sweep_and_prune(aabb_list):
    """
    Funkcija na osnovu liste Axis-aligned bounding boxa odredjuje potencijalne sudare.
    :param aabb_list: Lista Axis-aligned bounding box-ova.
    :type aabb_list: list[objects.AxisAlignedBoundingBox.AxisAlignedBoundingBox]
    :return: Lista potencijalnih sudara.
    :rtype: list[list[objects.AxisAlignedBoundingBox.AxisAlignedBoundingBox, objects.AxisAlignedBoundingBox.AxisAlignedBoundingBox]]
    """
    intervals = []
    intervals_start = []
    intervals_end = []
    for aabb in aabb_list:
        intervals.append(Interval(aabb))
        intervals_start.append(aabb.min_point.x)
        intervals_end.append(aabb.max_point.x)

    intervals = sort_intervals(intervals)
    intervals_start.sort()
    intervals_end.sort()

    i, j = 0, 0
    open_intervals = []
    possible_collisions = []
    while i < len(intervals_start) and j < len(intervals_end):
        if intervals_end[j] < intervals_start[i]:
            for interval in intervals:
                if interval.is_open() and interval.end == intervals_end[j]:
                    interval.close()
                    open_intervals.remove(interval)
                    break
            j += 1
        elif intervals_start[i] <= intervals_end[j]:
            intervals[i].open()
            for interval in open_intervals:
                possible_collisions.append([interval.object, intervals[i].object])
            open_intervals.append(intervals[i])
            i += 1

    for interval in open_intervals:
        interval.close()

    return possible_collisions


def ball_to_line_collision(line, ball):
    """
    Funkcija za proveravanje sudara kruga i duzi.
    :param line: Duz.
    :type line: objects.LinearBullet.LinearBullet
    :param ball: Krug.
    :type ball: objects.Ball.Ball
    :return: Podatak da li je doslo do sudara i vektor intenziteta sudara.
    :rtype: bool, object.Vector
    """
    A = line.get_min_coordinates()
    D = line.get_max_coordinates()
    C = ball.center

    A = Vector(A[0], A[1])
    D = Vector(D[0], D[1])
    statement = (A.x - C.x)**2 + (A.y - C.y)**2 <= ball.r**2
    if statement:
        Bx = np.sqrt(ball.r**2 - (A.y - C.y)**2) + C.x
        B = Vector(Bx, A.y)
        AB = B - A
        ab_normalized = AB.to_np_array()/np.linalg.norm(AB.to_np_array())
        ab_normalized_vector = Vector(ab_normalized[0], ab_normalized[1])
        ab_magnitude = np.sqrt(dot(AB, AB))
        return statement, ab_normalized_vector * ab_magnitude

    statement = (D.x - C.x) ** 2 + (D.y - C.y) ** 2 <= ball.r ** 2
    if statement:
        Bx = np.sqrt(ball.r ** 2 - (D.y - C.y) ** 2) + C.x
        B = Vector(Bx, D.y)
        DB = B - D
        db_normalized = DB.to_np_array() / np.linalg.norm(DB.to_np_array())
        db_normalized_vector = Vector(db_normalized[0], db_normalized[1])
        db_magnitude = np.sqrt(dot(DB, DB))
        return statement, db_normalized_vector * db_magnitude
    return False, -1


def ball_to_ball_collision(ball1, ball2):
    """
    Funkcija za proveravanje sudara dva kruga.
    :param ball1: Krug 1.
    :type ball1: objects.Ball.Ball or objects.Bomb.Bomb
    :param ball2: Krug 2.
    :type ball2: objects.Ball.Ball or objects.Bomb.Bomb
    :return: Podatak da li je doslo do sudara i vektor intenziteta sudara.
    :rtype: bool, object.Vector
    """
    C1 = ball1.center
    C2 = ball2.center
    support_v = C2 - C1
    v_normalized = support_v.to_np_array()/np.linalg.norm(support_v.to_np_array())
    v_normalized_vector = Vector(v_normalized[0], v_normalized[1])
    support_v_magnitude = np.sqrt(dot(support_v, support_v))
    return support_v_magnitude <= ball1.r + ball2.r, v_normalized_vector * support_v_magnitude


def support_function(vector, object1, object2):
    """
    Support funkcija za odredjivanje tacke na Minkowski razlici.
    :param vector: Vektor pravca za odredjivanje support tacke na objektima.
    :type vector: objects.Vector
    :param object1: Objekat 1.
    :type object1: objects.Ball.Ball or objects.Bomb.Bomb or objects.LinearBullet.LinearBullet or objects.Obstacle.Obstacle
    :param object2: Objekat 2.
    :type object2: objects.Ball.Ball or objects.Bomb.Bomb or objects.LinearBullet.LinearBullet or objects.Obstacle.Obstacle
    :return: Tacku na Minkowski razlici za zadati vektor.
    :rtype: object.Vector
    """
    # za sve vrste objekata moramo implementirati funkciju furthest_point(vector) koja ce nam vracati tacku koja je
    # najudaljenija tacka tog tela u odnosu na taj vector
    a = object1.furthest_point(vector)
    b = object2.furthest_point(vector * -1)
    return object1.furthest_point(vector) - object2.furthest_point(vector * -1)


def line_case(simplex, vector):
    """
    Funkcija koja dodaje trecu tacku na simplex Minkowski razlike.
    :param simplex: Lista koja sadrzi tacke koje se vec nalaze na simpleksu.
    :type simplex: list[objects.Vector.Vector]
    :param vector: Vektor pravca.
    :type vector: objects.Vector.Vector
    :return: Informaciju da li se tacka (0,0) nalazi unutar simpleksa.
    :rtype: bool
    """
    b, a = simplex[0], simplex[1]
    ab, ao = b - a, ORIGIN - a
    if np.linalg.norm(ab.to_np_array()) == 0:
        return True
    ab_normalized = ab.to_np_array()/np.linalg.norm(ab.to_np_array())
    ab_normalized_vector = Vector(ab_normalized[0], ab_normalized[1])
    ao_normalized = ao.to_np_array() / np.linalg.norm(ao.to_np_array())
    ao_normalized_vector = Vector(ao_normalized[0], ao_normalized[1])
    if ab_normalized_vector == ao_normalized_vector:
        return True
    ab_norm = triple_product(ab, ao, ab)
    if np.linalg.norm(ab_norm.to_np_array()) == 0:
        return True
    ab_norm_normalized = ab_norm.to_np_array()/np.linalg.norm(ab_norm.to_np_array())
    vector.set(ab_norm_normalized[0], ab_norm_normalized[1])
    return False


def triangle_case(simplex, vector):
    """
    Funkcija zamenjuje jednu tacku na simplexu sa novom.
    :param simplex: Lista koja sadrzi tacke koje se vec nalaze na simpleksu.
    :type simplex: list[objects.Vector.Vector]
    :param vector: Vektor pravca.
    :type vector: objects.Vector.Vector
    :return: Informaciju da li se tacka (0,0) nalazi unutar simpleksa.
    :rtype: bool
    """
    c, b, a = simplex[0], simplex[1], simplex[2]
    ab, ac, ao = b - a, c - a, ORIGIN - a

    ab_norm = triple_product(ab, ac, ab)
    if np.linalg.norm(ab_norm.to_np_array()) == 0:
        return ab_norm
    ab_norm_normalized = ab_norm.to_np_array()/np.linalg.norm(ab_norm.to_np_array())
    ab_norm_normalized_vector = Vector(ab_norm_normalized[0], ab_norm_normalized[1])

    ac_norm = triple_product(ac, ab, ac)
    if np.linalg.norm(ac_norm.to_np_array()) == 0:
        return ac_norm
    ac_norm_normalized = ac_norm.to_np_array()/np.linalg.norm(ac_norm.to_np_array())
    ac_norm_normalized_vector = Vector(ac_norm_normalized[0], ac_norm_normalized[1])

    if dot(ab_norm_normalized_vector, ao) > 0:
        simplex.remove(c)
        vector.set(ab_norm_normalized[0], ab_norm_normalized[1])
        return False
    elif dot(ac_norm_normalized_vector, ao) > 0:
        simplex.remove(b)
        vector.set(ac_norm_normalized[0], ac_norm_normalized[1])
        return False
    return True


def handle_simplex(simplex, vector):
    """
    Funkcija na osnovu duzine liste simpleksa odredjuje da li ce se pozvati line_case ili trianle_case funkcija.
    :param vector: Vektor pravca za odredjivanje support tacke na objektima.
    :param simplex: Lista koja sadrzi tacke koje se vec nalaze na simpleksu.
    :type simplex: list[objects.Vector.Vector]
    :param vector: Vektor pravca.
    :type vector: objects.Vector.Vector
    :return: Informaciju da li se tacka (0,0) nalazi unutar simpleksa.
    :rtype: bool
    """
    if len(simplex) == 2:
        return line_case(simplex, vector)
    return triangle_case(simplex, vector)


def gjk(object1, object2, side):
    """
    Gilbert–Johnson–Keerthi algoritam za detekciju kolizija.
    :param object1: Objekat 1.
    :type object1: objects.Ball.Ball or objects.Bomb.Bomb or objects.LinearBullet.LinearBullet or objects.Obstacle.Obstacle
    :param object2: Objekat 2.
    :type object2: objects.Ball.Ball or objects.Bomb.Bomb or objects.LinearBullet.LinearBullet or objects.Obstacle.Obstacle
    :param side: Podatak sa koje strane se desava potencijalni sudar
     (moguce vreddnosti: 0 - sa leve strane; 1 - sa desne).
    :type side: int
    :return: Podatak da li je doslo do sudara i vektor intenziteta sudara.
    :rtype: bool, objects.Vector
    """
    # moramo imati centar svih vrsta tela koje definisemo!!
    support_v = object2.center - object1.center
    d = support_v.to_np_array() / np.linalg.norm(support_v.to_np_array())
    d = Vector(d[0], d[1])
    simplex = [support_function(d, object1, object2)]
    if side == 0:
        support_v = ORIGIN - simplex[0]
    elif side == 1:
        support_v = simplex[0] - ORIGIN
    if support_v == ORIGIN:
        return True, 1
    v_normalized = support_v.to_np_array() / np.linalg.norm(support_v.to_np_array())
    d.set(v_normalized[0], v_normalized[1])
    while True:
        A = support_function(d, object1, object2)
        # sanity check
        if dot(d, A) < 0:
            return False, -1
        simplex.append(A)
        if handle_simplex(simplex, d):
            dist = None
            if len(simplex) == 3:
                dist = epa(simplex, object1, object2)
            return True, dist


def add_vertex(simplex, min_index, vector):
    """
    Funkcija dodaje tacku u simpleks.
    :param simplex: Lista tacaka simpleksa.
    :type simplex: list[objects.Vector.Vector]
    :param min_index: Mesto u listi za novu tacku.
    :type min_index: int
    :param vector: Vektor pravca.
    :type vector: objects.Vector.Vector
    """
    if min_index + 1 == len(simplex):
        simplex.append(vector)
        return
    temp = simplex[min_index+1]
    simplex[min_index+1] = vector
    for i in range(min_index+2, len(simplex)):
        simplex[i], temp = temp, simplex[i]
    simplex.append(temp)


def epa(simplex, object1, object2):
    """
    Expanding polytope algoritam.
    :param simplex: Lista tacaka simpleksa.
    :type simplex: list[objects.Vector.Vector]
    :param object1: Objekat 1.
    :type object1: objects.Ball.Ball or objects.Bomb.Bomb or objects.LinearBullet.LinearBullet or objects.Obstacle.Obstacle
    :param object2: Objekat 2.
    :type object2: objects.Ball.Ball or objects.Bomb.Bomb or objects.LinearBullet.LinearBullet or objects.Obstacle.Obstacle
    :return: Vektor intenziteta sudara.
    :rtype: object.Vector.Vector
    """
    min_dist = np.Inf
    min_index = 0
    min_norm = None

    while np.isinf(min_dist):
        for i in range(len(simplex)):
            j = (i+1) % len(simplex)
            a, b = simplex[i], simplex[j]

            ab, ao = b - a, ORIGIN - a

            ab_norm = triple_product(ab, a, ab)
            if np.linalg.norm(ab_norm.to_np_array()) == 0:
                return ab_norm
            ab_norm_normalized = ab_norm.to_np_array() / np.linalg.norm(ab_norm.to_np_array())
            ab_norm_normalized_vector = Vector(ab_norm_normalized[0], ab_norm_normalized[1])

            dist = dot(a, ab_norm_normalized_vector)
            if dist < 0:
                dist *= -1
                ab_norm_normalized_vector = ab_norm_normalized_vector * -1

            if dist < min_dist:
                min_dist = dist
                min_index = i
                min_norm = ab_norm_normalized_vector

        support_v = support_function(min_norm, object1, object2)
        if support_v in simplex:
            break
        v_normalized = support_v.to_np_array() / np.linalg.norm(support_v.to_np_array())
        v_normalized_vector = Vector(v_normalized[0], v_normalized[1])
        if abs(dist - dot(v_normalized_vector, min_norm)) > 0.001:
            add_vertex(simplex, min_index, support_v)
            min_dist = np.Inf

    return min_norm


def check_for_collisions(object_list):
    """
    Funkcija za detekciju kolizija.
    :param object_list: Lista svih objekata.
    :type object_list: list[objects.Ball.Ball or objects.Bomb.Bomb or objects.LinearBullet.LinearBullet or objects.Obstacle.Obstacle]
    :return: Lista kolizija.
    :rtype: list[list[objects.AxisAlignedBoundingBox.AxisAlignedBoundingBox, objects.AxisAlignedBoundingBox.AxisAlignedBoundingBox, objects.Vector.Vector]]
    """
    aabb_list = []
    collisions = []
    for shape in object_list:
        aabb_list.append(AxisAlignedBoundingBox(shape))

    possible_collisions = sweep_and_prune(aabb_list)

    for possible_collision in possible_collisions:
        aabb1 = possible_collision[0]
        aabb2 = possible_collision[1]
        if aabb1.overlap_check(aabb2):
            if isinstance(aabb1.shape, LinearBullet) and isinstance(aabb2.shape, Ball):
                collide, vector = ball_to_line_collision(aabb1.shape, aabb2.shape)
                if collide:
                    possible_collision.append(vector)
                    collisions.append(possible_collision)
            elif isinstance(aabb2.shape, LinearBullet) and isinstance(aabb1.shape, Ball):
                collide, vector = ball_to_line_collision(aabb2.shape, aabb1.shape)
                if collide:
                    possible_collision.append(vector)
                    collisions.append(possible_collision)
            elif isinstance(aabb1.shape, Bomb) and isinstance(aabb2.shape, Ball) or\
                    isinstance(aabb1.shape, Ball) and isinstance(aabb2.shape, Bomb):
                collide, vector = ball_to_ball_collision(aabb1.shape, aabb2.shape)
                if collide:
                    possible_collision.append(vector)
                    collisions.append(possible_collision)
            elif isinstance(aabb1.shape, (Bomb, LinearBullet)) and isinstance(aabb2.shape, Obstacle) or\
                    isinstance(aabb2.shape,  (Bomb, LinearBullet)) and isinstance(aabb1.shape, Obstacle):
                collide, vector = gjk(possible_collision[0].shape, possible_collision[1].shape, 1)
                if collide:
                    possible_collision.append(vector)
                    collisions.append(possible_collision)
            elif isinstance(aabb1.shape, Ball) and isinstance(aabb2.shape, Obstacle) or\
                    isinstance(aabb2.shape, Ball) and isinstance(aabb1.shape, Obstacle):
                collide, vector = gjk(possible_collision[0].shape, possible_collision[1].shape, 0)
                if collide:
                    possible_collision.append(vector)
                    collisions.append(possible_collision)
    return collisions


def resolve_collisions(collision_list, object_list, terrain):
    """
    Funkcija za reakciju na kolizije.
    :param collision_list: Lista kolizija.
    :type collision_list: list[list[objects.AxisAlignedBoundingBox.AxisAlignedBoundingBox, objects.AxisAlignedBoundingBox.AxisAlignedBoundingBox, objects.Vector.Vector]]
    :param object_list: Lista objekata.
    :type object_list: list[objects.Ball.Ball or objects.Bomb.Bomb or objects.LinearBullet.LinearBullet or objects.Obstacle.Obstacle]
    :param terrain: Podloga.
    :type terrain: list[tuple]
    :return: Informacija da li je doslo do kraja igre.
    :rtype: bool
    """
    for collision in collision_list:
        object1 = collision[0].shape
        object2 = collision[1].shape
        vector = collision[2]

        if isinstance(object1, Bomb) and isinstance(object2, Ball):
            # return True
            return False
        if isinstance(object1, LinearBullet) and isinstance(object2, Ball):
            # return True
            collision_reaction_bullet(object2, object1)
            object_list.remove(object1)
        elif isinstance(object2, Bomb) and isinstance(object1, Ball):
            # return True
            return False
        elif isinstance(object2, LinearBullet) and isinstance(object1, Ball):
            # return True
            collision_reaction_bullet(object1, object2)
            object_list.remove(object2)
        elif isinstance(object1, (Bomb, LinearBullet)) and isinstance(object2, Obstacle):
            try:
                object_list.remove(object1)
            except ValueError:
                pass
        elif isinstance(object2, (Bomb, LinearBullet)) and isinstance(object1, Obstacle):
            try:
                object_list.remove(object2)
            except ValueError:
                pass
        elif isinstance(object1, Ball) and isinstance(object2, Obstacle):
            terrain_vector = Vector(terrain[1][0], terrain[1][1]) - Vector(terrain[0][0], terrain[0][1])
            most_left_point = object2.furthest_point(terrain_vector)
            terrain_vector = most_left_point - object2.center
            angle = np.arccos(dot(terrain_vector, vector)/(magnitude(terrain_vector)*magnitude(vector)))

            side_number = angle//(2*np.pi/object2.number_of_sides)
            # print(side_number)

            # nad leom (object1) treba napraviti odbijanje
            collision_reaction_polygon(object1, side_number-2, object2.number_of_sides, object_list, terrain)
        elif isinstance(object2, Ball) and isinstance(object1, Obstacle):
            terrain_vector = Vector(terrain[1][0], terrain[1][1]) - Vector(terrain[0][0], terrain[0][1])
            most_left_point = object2.furthest_point(terrain_vector)
            terrain_vector = most_left_point - object2.center
            angle = np.arccos(dot(terrain_vector, vector)/(magnitude(terrain_vector)*magnitude(vector)))

            side_number = 1 + angle//(2*np.pi/object1.number_of_sides)
            # print(side_number)

            # nad leom (object2) treba napraviti odbijanje
            collision_reaction_polygon(object2, side_number-2, object1.number_of_sides, object_list, terrain)

    return True
