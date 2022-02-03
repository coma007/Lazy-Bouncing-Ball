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
    run = True
    binary_terrain = create_terrain()
    terrain = []

    for coordinates, ground in binary_terrain.items():
        if ground:
            WIDTH, LENGTH = pygame.display.get_surface().get_size()
            x, y = coordinates
            pygame.draw.rect(surface, ground_color, pygame.Rect(x, y+400, 10000/WIDTH, 10000/LENGTH), 2)
            terrain.append((x, y+400))

    while run:
        # for o in objects:
        #     if isinstance(o, Ball):
        #         continue
        #     o.x += 30

        if random.random() < 0.1:
            i = random.randint(0, 3)
            if i == 0:
                objects.append(Bomb(700))
            elif i == 1:
                objects.append(LinearBullet(500))
            else:
                j = random.randint(3, 11)
                objects.append(Obstacle(300, j))

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
                pygame.draw.line(surface, o.color, o.get_min_coordinates(), o.get_max_coordinates())
            elif isinstance(o, Obstacle):
                pygame.draw.polygon(surface, o.color, o.get_all_vertices())

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            speed_up_ball(leo)

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            slow_down_ball(leo)
        if pygame.key.get_pressed()[pygame.K_UP]:
            leo.jumping = True
            jump_ball(leo)
        else:
            if leo.v_h > 0:
                # SVAKO TIJELO PREPUSTENO SAMOM SEBI
                # TEZI STANJU MIROVANJA
                # ILI RAVNOMJERNOG PRAVOLINIJSKOG KRETANJA
                inertion(leo)
                leo.x += leo.v_h * (1-0)
            pygame.draw.circle(surface, leo.color, leo.coor, leo.r)

        collisions = check_for_collisions(objects)
        print(collisions)
        run = resolve_collisions(collisions)
        pygame.display.update()
    pygame.quit()
