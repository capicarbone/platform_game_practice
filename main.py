from typing import List, Dict
import os, random

import pygame, sys
from pygame.locals import *

class PlayerModel(pygame.Rect):
    def __init__(self, left, top):
        super().__init__(left, top, 26, 32)
        self.y_momentum = 0


pygame.mixer.pre_init(44100, -16, 2, 512)


clock = pygame.time.Clock()
pygame.init()
pygame.mixer.set_num_channels(64)
pygame.display.set_caption('Pygame window')

WINDOWS_SIZE = (1200, 800)

screen = pygame.display.set_mode(WINDOWS_SIZE, 0, 32)

display = pygame.Surface((600, 400))

grass_image = pygame.image.load('grass.png')
dirt_image = pygame.image.load('dirt.png')
r_corner_image = pygame.image.load('right_corner.png')
l_corner_image = pygame.image.load('left_corner.png')

jump_sound = pygame.mixer.Sound('jump.wav')
grass_sounds = [pygame.mixer.Sound('grass_0.wav'), pygame.mixer.Sound('grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)

TILE_SIZE = grass_image.get_height()

true_scroll = [0, 0]

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))

    return game_map

global animation_frames
animation_frames = {}

def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 1
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc)
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1

    return animation_frame_data

def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame

animation_database = {}
animation_database['idle'] = load_animation('player_animations/idle', [10, 10, 10, 10])
animation_database['walk'] = load_animation('player_animations/walk', [7, 7, 7, 7, 7, 7])

player_action = 'idle'
player_frame = 0
player_flip = False

grass_sound_timer = 0

game_map = load_map('map')

background_objects = [[0.25,[120,20,140,400]],[0.25,[400,120,80,400]],[0.5,[60,80,80,400]],[0.5,[260,180,200,400]],[0.5,[600,160,240,800]]]

def collision_test(rect: Rect, tiles: List[Rect]):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect: PlayerModel, movement: Dict, tiles: List[Rect]) -> (Rect, Dict):
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

player = PlayerModel(50, 50)
test_rect = pygame.Rect(100, 100, 100, 50)

moving_right = False
moving_left = False
air_time = 0

while True:
    display.fill((146, 244, 255))

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    true_scroll[0] += (player.x - true_scroll[0] - int((display.get_width() / 2)) + int(player.width / 2)) / 20
    true_scroll[1] += (player.y - true_scroll[1] - int(display.get_height() / 2)) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display, (7, 80, 75),
                     pygame.Rect(0, display.get_height() * 0.65, screen.get_width(), display.get_height() * 0.35))

    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0], background_object[1][1]-scroll[1]*background_object[0], background_object[1][2], background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (14, 222, 150), obj_rect)
        else:
            pygame.draw.rect(display, (9, 91, 85), obj_rect)

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            tile_position = (x * TILE_SIZE - true_scroll[0], y * TILE_SIZE - true_scroll[1])
            if tile == '1':
                display.blit(dirt_image, tile_position)
            if tile == '2':
                display.blit(grass_image, tile_position)
            if tile == '3':
                display.blit(r_corner_image, tile_position)
            if tile == '4':
                display.blit(l_corner_image, tile_position)
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

            x += 1
        y += 1

    player_movement = [0,0]
    if moving_right:
        player_movement[0] += 4
    if moving_left:
        player_movement[0] -= 4
    player_movement[1] += player.y_momentum
    player.y_momentum += 0.4
    if player.y_momentum > 9:
        player.y_momentum = 9

    if player_movement[0] > 0:
        player_action, player_frame = change_action(player_action, player_frame, 'walk')
        player_flip = False

    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')

    if player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'walk')
        player_flip = True

    player, collisions = move(player, player_movement, tile_rects)

    if collisions['bottom']:
        player.y_momentum = 0
        air_time = 0
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()
    else:
        air_time += 1

    if collisions['top']:
        player.y_momentum = -player.y_momentum

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_image = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_image, player_flip, False), (player.x - true_scroll[0], player.y - true_scroll[1]))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_e:
                pygame.mixer.music.play(-1)
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_time < 6:
                    jump_sound.play()
                    player.y_momentum = -9

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOWS_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)
