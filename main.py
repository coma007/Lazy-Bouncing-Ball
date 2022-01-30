import pygame
from objects.Ball import *
from terrain import *
from physics import *


if __name__ == '__main__':

    sky_color = (135, 206, 235)
    ground_color = (212, 123, 74)

    pygame.init()
    pygame.display.set_caption("Game")
    surface = pygame.display.set_mode((1000, 600))
    surface.fill(sky_color)

    clock = pygame.time.Clock()

    leo = Ball()
    run = True
    binary_terrain = create_terrain()
    terrain = []

    for coordinates, ground in binary_terrain.items():
        if ground:
            WIDTH, LENGTH = pygame.display.get_surface().get_size()
            x, y = coordinates
            pygame.draw.rect(surface, ground_color, pygame.Rect(x, y+400, 10000/WIDTH, 10000/LENGTH), 2)
            terrain.append((x, y+400))

    leo.do_gravity(terrain)
    pygame.draw.circle(surface, leo.color, leo.coor, leo.r)
    while run:
        pygame.draw.circle(surface, sky_color, leo.coor, leo.r)
        clock.tick(leo.v[1]+60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            speed_up_ball(leo)
            pygame.draw.circle(surface, leo.color, leo.coor, leo.r)
            print(leo.coor)
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            slow_down_ball(leo)
        if pygame.key.get_pressed()[pygame.K_UP]:
            jump_ball(leo)
        else:
            pygame.draw.circle(surface, leo.color, leo.coor, leo.r)
        pygame.display.update()
    pygame.quit()
