import pygame
from objects.Ball import *
from objects.Bomb import Bomb
from objects.Obstacle import Obstacle
from utils.collision import check_for_collisions
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
    bomb = Bomb(500)
    obstacle1 = Obstacle(600)
    obstacle2 = Obstacle(300, 4)
    objects = [leo, bomb, obstacle1, obstacle2]
    bullet = LinearBullet(700)
    objects.append(bullet)
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
        clock.tick(np.abs(leo.v[0])+10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if not leo.jumping:
            leo.do_gravity(terrain)
        pygame.draw.circle(surface, sky_color, leo.coor, leo.r)
        pygame.draw.circle(surface, bomb.color, bomb.coor, bomb.r)
        pygame.draw.line(surface, bullet.color, bullet.get_min_coordinates(), bullet.get_max_coordinates())
        pygame.draw.polygon(surface, obstacle1.color, obstacle1.get_all_vertices())
        pygame.draw.polygon(surface, obstacle2.color, obstacle2.get_all_vertices())

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
        pygame.display.update()
    pygame.quit()
