from typing import List, Dict

import pygame, sys
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Pygame window')

WINDOWS_SIZE = (1200, 800)

screen = pygame.display.set_mode(WINDOWS_SIZE, 0, 32)

display = pygame.Surface((600, 400))

player_image = pygame.image.load('character.png')
grass_image = pygame.image.load('grass.png')
dirt_image = pygame.image.load('dirt.png')
r_corner_image = pygame.image.load('right_corner.png')
l_corner_image = pygame.image.load('left_corner.png')

TILE_SIZE = grass_image.get_height()

game_map = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '2', '2', '2', '2', '2', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['2', '3', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '4', '2'],
            ['1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']]


def collision_test(rect: Rect, tiles: List[Rect]):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect: Rect, movement: Dict, tiles: List[Rect]) -> (Rect, Dict):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types


player_y_momentun = 0

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)

moving_right = False
moving_left = False
air_time = 0

while True:
    display.fill((146, 244, 255))

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '3':
                display.blit(r_corner_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '4':
                display.blit(l_corner_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

            x += 1
        y += 1





    player_movement = [0,0]
    if moving_right:
        player_movement[0] += 4
    if moving_left:
        player_movement[0] -= 4
    player_movement[1] += player_y_momentun
    player_y_momentun += 0.4
    if player_y_momentun > 9:
        player_y_momentun = 9

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentun = 0
        air_time = 0
    else:
        air_time += 1

    if collisions['top']:
        player_y_momentun = -player_y_momentun

    display.blit(player_image, (player_rect.x, player_rect.y))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_time < 6:
                    player_y_momentun = -9

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOWS_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)
