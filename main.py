import pygame, random
from objects.Ball import *
from objects.Bomb import Bomb
from objects.Obstacle import Obstacle
from utils.collision import check_for_collisions, resolve_collisions
from utils.terrain.terrain import *
from utils.physics import *
from objects.LinearBullet import *


if __name__ == '__main__':

    sky_color = (135, 206, 235)
    ground_color = (212, 123, 74)

    pygame.init()
    pygame.display.set_caption("Game")
    surface = pygame.display.set_mode((1000, 600))
    surface.fill(sky_color)

    clock = pygame.time.Clock()

    leo = Ball()
    objects = [leo]
    number_of_objects = 0
    spawn_rate = 0.007

    run = True
    binary_terrain = create_terrain()
    terrain = []

    for coordinates, ground in binary_terrain.items():
        if ground:
            WIDTH, LENGTH = pygame.display.get_surface().get_size()
            x, y = coordinates
            pygame.draw.rect(surface, ground_color, pygame.Rect(x, y+400, 10000/WIDTH, 10000/LENGTH), 2)
            terrain.append((x, y+400))

    objects.append(Bomb(700))
    #
    # j = random.randint(3, 11)
    objects.append(Obstacle(1000, 4))
    #
    # objects.append(LinearBullet(1000))
    while run:
        if number_of_objects == 10:
            number_of_objects = 0
            spawn_rate *= 1.2
        if random.random() < spawn_rate and len(objects) < 5:
            i = random.randint(0, 3)
            if i == 0:
                objects.append(Bomb(1100))
                number_of_objects += 1
            elif i == 1:
                objects.append(LinearBullet(1200))
                number_of_objects +=1
            else:
                j = random.randint(0,2)
                if j == 0:
                    objects.append(Obstacle(1400, 4))
                elif j == 1:
                    objects.append(Obstacle(1400, 6))
                number_of_objects += 1

        clock.tick(np.abs(leo.v[0])+10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if not run:
            break

        if not leo.jumping:
            leo.do_gravity(terrain)

        for o in objects:
            if isinstance(o, (Ball, Bomb)):
                pygame.draw.circle(surface, sky_color, o.coor, o.r)
            elif isinstance(o, LinearBullet):
                pygame.draw.line(surface, sky_color, o.get_min_coordinates(), o.get_max_coordinates())
            elif isinstance(o, Obstacle):
                pygame.draw.polygon(surface, sky_color, o.get_all_vertices())
                a = o.get_min_coordinates()
                for x in range(int(o.get_min_coordinates()[0]), int(o.get_max_coordinates()[0]) + 1):
                    y_0 = terrain[0][1]
                    for y in range(y_0, int(o.get_max_coordinates()[1]) + 1):
                        WIDTH, LENGTH = pygame.display.get_surface().get_size()
                        # y = terrain[0][1]
                        pygame.draw.rect(surface, ground_color,
                                         pygame.Rect(x, y, 10000 / WIDTH, 10000 / LENGTH), 2)

        if pygame.key.get_pressed()[pygame.K_RIGHT] and not leo.jumping:
            speed_up_ball_ground(leo, objects)
            if pygame.key.get_pressed()[pygame.K_UP]:
                leo.jumping = True
            for o in objects:
                if isinstance(o, LinearBullet):
                    pygame.draw.line(surface, sky_color, o.get_min_coordinates(), o.get_max_coordinates())
                    o.get_position(leo)
                elif isinstance(o, Bomb):
                    pygame.draw.circle(surface, sky_color, o.coor, o.r)
                    o.get_position(leo)
                elif isinstance(o, Obstacle):
                    pygame.draw.polygon(surface, sky_color, o.get_all_vertices())
                    for x in range(int(o.get_min_coordinates()[0]), int(o.get_max_coordinates()[0]) + 1):
                        y_0 = terrain[0][1]
                        for y in range(y_0, int(o.get_max_coordinates()[1]) + 1):
                            WIDTH, LENGTH = pygame.display.get_surface().get_size()
                            # y = terrain[0][1]
                            pygame.draw.rect(surface, ground_color,
                                             pygame.Rect(x, y, 10000 / WIDTH, 10000 / LENGTH), 2)
                    o.get_position(leo)
                if o.x < 0:
                    objects.remove(o)
            # collisions = check_for_collisions(objects)
            #
            # # print(collisions)
            # run = resolve_collisions(collisions, objects)
        elif pygame.key.get_pressed()[pygame.K_LEFT] and not leo.jumping:
            slow_down_ball_ground(leo, objects)
            if pygame.key.get_pressed()[pygame.K_UP]:
                leo.jumping = True
            for o in objects:
                if isinstance(o, LinearBullet):
                    pygame.draw.line(surface, sky_color, o.get_min_coordinates(), o.get_max_coordinates())
                    o.get_position(leo)
                elif isinstance(o, Bomb):
                    pygame.draw.circle(surface, sky_color, o.coor, o.r)
                    o.get_position(leo)
                elif isinstance(o, Obstacle):
                    pygame.draw.polygon(surface, sky_color, o.get_all_vertices())
                    for x in range(int(o.get_min_coordinates()[0]), int(o.get_max_coordinates()[0]) + 1):
                        y_0 = terrain[0][1]
                        for y in range(y_0, int(o.get_max_coordinates()[1]) + 1):
                            WIDTH, LENGTH = pygame.display.get_surface().get_size()
                            # y = terrain[0][1]
                            pygame.draw.rect(surface, ground_color,
                                             pygame.Rect(x, y, 10000 / WIDTH, 10000 / LENGTH), 2)
                    o.get_position(leo)
                if o.x < 0:
                    objects.remove(o)
            # collisions = check_for_collisions(objects)
        elif pygame.key.get_pressed()[pygame.K_UP] and not leo.jumping:
            leo.jumping = True
        if leo.jumping:
            jump(leo, terrain, objects)
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                speed_up_ball(leo, objects)
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                slow_down_ball(leo, objects)
            for o in objects:
                if isinstance(o, LinearBullet):
                    pygame.draw.line(surface, sky_color, o.get_min_coordinates(), o.get_max_coordinates())
                elif isinstance(o, Bomb):
                    pygame.draw.circle(surface, sky_color, o.coor, o.r)
                elif isinstance(o, Obstacle):
                    pygame.draw.polygon(surface, sky_color, o.get_all_vertices())
                    for x in range(int(o.get_min_coordinates()[0]), int(o.get_max_coordinates()[0]) + 1):
                        y_0 = terrain[0][1]
                        for y in range(y_0, int(o.get_max_coordinates()[1]) + 1):
                            WIDTH, LENGTH = pygame.display.get_surface().get_size()
                            # y = terrain[0][1]
                            pygame.draw.rect(surface, ground_color,
                                             pygame.Rect(x, y, 10000 / WIDTH, 10000 / LENGTH), 2)
                if o.x < 0:
                    objects.remove(o)

            for o in objects:
                if isinstance(o, Bomb):
                    pygame.draw.circle(surface, o.color, o.coor, o.r)
                elif isinstance(o, LinearBullet):
                    pygame.draw.line(surface, o.color, o.get_min_coordinates(), o.get_max_coordinates())
                elif isinstance(o, Obstacle):
                    pygame.draw.polygon(surface, o.color, o.get_all_vertices())
            # collisions = check_for_collisions(objects)
            #
            # # print(collisions)
            # run = resolve_collisions(collisions, objects)
        elif not leo.jumping:
            if leo.v_h > 0:
                # SVAKO TIJELO PREPUSTENO SAMOM SEBI
                # TEZI STANJU MIROVANJA
                # ILI RAVNOMJERNOG PRAVOLINIJSKOG KRETANJA
                inertion(leo)
                # leo.x += leo.v_h * (1-0)
            # pygame.draw.circle(surface, leo.color, leo.coor, leo.r)
            for o in objects:
                if isinstance(o, LinearBullet):
                    pygame.draw.line(surface, sky_color, o.get_min_coordinates(), o.get_max_coordinates())
                    o.get_position(leo)
                elif isinstance(o, Bomb):
                    pygame.draw.circle(surface, sky_color, o.coor, o.r)
                    o.get_position(leo)
                elif isinstance(o, Obstacle):
                    pygame.draw.polygon(surface, sky_color, o.get_all_vertices())
                    for x in range(int(o.get_min_coordinates()[0]), int(o.get_max_coordinates()[0]) + 1):
                        y_0 = terrain[0][1]
                        for y in range(y_0, int(o.get_max_coordinates()[1]) + 1):
                            WIDTH, LENGTH = pygame.display.get_surface().get_size()
                            # y = terrain[0][1]
                            pygame.draw.rect(surface, ground_color,
                                             pygame.Rect(x, y, 10000 / WIDTH, 10000 / LENGTH), 2)
                    o.get_position(leo)
                if o.x < 0:
                    objects.remove(o)

        collisions = check_for_collisions(objects)

        # print(collisions)
        run = resolve_collisions(collisions, objects, terrain)

        pygame.draw.circle(surface, leo.color, leo.coor, leo.r)

        for o in objects:
            if isinstance(o, Bomb):
                pygame.draw.circle(surface, o.color, o.coor, o.r)
            elif isinstance(o, LinearBullet):
                pygame.draw.line(surface, o.color, o.get_min_coordinates(), o.get_max_coordinates())
            elif isinstance(o, Obstacle):
                pygame.draw.polygon(surface, o.color, o.get_all_vertices())

        pygame.display.update()
    pygame.quit()
