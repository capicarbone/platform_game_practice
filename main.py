import random
from typing import List, Dict, Tuple
from collections import namedtuple

import pygame, sys
from pygame.locals import *

Point = namedtuple('Point', ['x', 'y'])


def collision_test(rect: Rect, tiles: List[Rect]):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


class Controller(object):
    def reacto_to(self, event: pygame.event.Event):
        pass

    def update(self):
        pass

    def draw(self, display: pygame.Surface, scroll: Point):
        pass


class CameraModel(object):
    def __init__(self, width: int, height: int, following: Rect):
        self.x_offset = 0
        self.y_offset = 0
        self.width = width
        self.height = height
        self.following = following


class CameraController(Controller):
    def __init__(self, camera: CameraModel):
        self.camera = camera

    def update(self):
        self.camera.x_offset += (self.camera.following.x - self.camera.x_offset - int((self.camera.width / 2)) + int(
            self.camera.following.width / 2)) / 20
        self.camera.y_offset += (self.camera.following.y - self.camera.y_offset - int(self.camera.height / 2)) / 20

    def get_camera_position(self):
        return Point(int(self.camera.x_offset), int(self.camera.y_offset))


class Tile(Rect):
    def __init__(self, left, top, width, height, type: str):
        super(Tile, self).__init__(left, top, width, height)
        self.type = type


class SceneryModel(object):
    def __init__(self, tiles: List[Tile]):
        self.tiles = tiles

    @staticmethod
    def from_map_file(path: str, tile_width: int, tile_height: int):
        f = open(path + '.txt', 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        game_map = []

        for row in data:
            game_map.append(list(row))

        tiles: List[Tile] = []
        for y in range(len(game_map)):
            for x in range(len(game_map[y])):
                if game_map[y][x] != '0':
                    tiles.append(Tile(x * tile_width, y * tile_height, tile_width, tile_height, game_map[y][x]))

        return SceneryModel(tiles)


class ScenaryView(object):
    def __init__(self):
        self.tiles_images = {}
        self.tiles_images['2'] = pygame.image.load('grass.png')
        self.tiles_images['1'] = pygame.image.load('dirt.png')
        self.tiles_images['3'] = pygame.image.load('right_corner.png')
        self.tiles_images['4'] = pygame.image.load('left_corner.png')

        self.background_objects = [[0.25, [120, 20, 140, 400]], [0.25, [400, 120, 80, 400]], [0.5, [60, 80, 80, 400]],
                                   [0.5, [260, 180, 200, 400]], [0.5, [600, 160, 240, 800]]]



    def render(self, display: pygame.Surface, scenary: SceneryModel, scroll):
        display.fill((146, 244, 255))

        pygame.draw.rect(display, (7, 80, 75),
                         pygame.Rect(0, display.get_height() * 0.65, display.get_width(), display.get_height() * 0.35))

        for background_object in self.background_objects:
            obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0],
                                   background_object[1][1] - scroll[1] * background_object[0], background_object[1][2],
                                   background_object[1][3])
            if background_object[0] == 0.5:
                pygame.draw.rect(display, (14, 222, 150), obj_rect)
            else:
                pygame.draw.rect(display, (9, 91, 85), obj_rect)

        for tile in scenary.tiles:
            tile_position = (tile.left - scroll[0], tile.top - scroll[1])
            display.blit(self.tiles_images[tile.type], tile_position)



class SceneryController(Controller):
    def __init__(self, scenery: SceneryModel, view: ScenaryView):
        self.scenary = scenery
        self.view = view

        pygame.mixer.music.load('music.wav')
        pygame.mixer.music.play(-1)

    def update(self):
        pass

    def draw(self, surface: pygame.Surface, scroll: Point):
        self.view.render(surface, self.scenery, scroll)

    def react_to(self, event: pygame.event.Event):
        if event.type == KEYDOWN:
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_e:
                pygame.mixer.music.play(-1)


class PlayerModel(pygame.Rect):
    def __init__(self, star_position: Tuple[int, int]):
        super().__init__(star_position[0], star_position[1], 26, 32)
        self.y_momentum = 0
        self.moving_right = False
        self.moving_left = False
        self.air_time = 0
        self.action = 'idle'
        self.front_to_right = True


class PlayerView(object):
    def __init__(self):
        self.player_action = 'idle'
        self.player_frame = 0
        self.animation_database = {}
        self.animation_frames = {}
        self.animation_database['idle'] = self._load_animation('player_animations/idle', [10, 10, 10, 10])
        self.animation_database['walk'] = self._load_animation('player_animations/walk', [7, 7, 7, 7, 7, 7])

    def _load_animation(self, path, frame_durations):

        animation_name = path.split('/')[-1]
        animation_frame_data = []
        n = 1
        for frame in frame_durations:
            animation_frame_id = animation_name + '_' + str(n)
            img_loc = path + '/' + animation_frame_id + '.png'
            animation_image = pygame.image.load(img_loc)
            self.animation_frames[animation_frame_id] = animation_image.copy()
            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1

        return animation_frame_data

    def _change_action(self, new_value):
        if self.player_action != new_value:
            self.player_action = new_value
            self.player_frame = 0

    def render(self, display: pygame.Surface, player: PlayerModel, scroll: Point):
        self._change_action(player.action)
        self.player_frame += 1
        if self.player_frame >= len(self.animation_database[self.player_action]):
            self.player_frame = 0
        player_img_id = self.animation_database[self.player_action][self.player_frame]
        player_image = self.animation_frames[player_img_id]
        display.blit(pygame.transform.flip(player_image, not player.front_to_right, False),
                     (player.x - scroll[0], player.y - scroll[1]))


class PlayerController(Controller):
    def __init__(self, player: PlayerModel, scenery: SceneryModel, view: PlayerView):
        self.player = player
        self.view = view
        self.scenery = scenery
        self.grass_sound_timer = 0
        self._load_sounds()

    def _load_sounds(self):
        self.jump_sound = pygame.mixer.Sound('jump.wav')
        self.grass_sounds = [pygame.mixer.Sound('grass_0.wav'), pygame.mixer.Sound('grass_1.wav')]
        self.grass_sounds[0].set_volume(0.2)
        self.grass_sounds[1].set_volume(0.2)

    def update(self):

        if self.grass_sound_timer > 0:
            self.grass_sound_timer -= 1

        movement = [0, 0]
        if self.player.moving_right:
            movement[0] += 4
        if self.player.moving_left:
            movement[0] -= 4
        movement[1] += self.player.y_momentum
        self.player.y_momentum += 0.4
        if self.player.y_momentum > 9:
            self.player.y_momentum = 9

        if movement[0] > 0:
            self.player.action = 'walk'
            self.player.front_to_right = True

        if movement[0] == 0:
            self.player.action = 'idle'

        if movement[0] < 0:
            self.player.action = 'walk'
            self.player.front_to_right = False

        collisions = self._move(movement)

        if collisions['bottom']:
            self.player.y_momentum = 0
            self.player.air_time = 0
            if movement[0] != 0:
                if self.grass_sound_timer == 0:
                    self.grass_sound_timer = 30
                    random.choice(self.grass_sounds).play()
        else:
            self.player.air_time += 1

        if collisions['top']:
            self.player.y_momentum = -self.player.y_momentum

    def _move(self, movement: List[int]) -> (Rect, Dict):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.player.x += movement[0]

        hit_list = collision_test(self.player, self.scenery.tiles)

        for tile in hit_list:
            if movement[0] > 0:
                self.player.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                self.player.left = tile.right
                collision_types['left'] = True
        self.player.y += movement[1]
        hit_list = collision_test(self.player, self.scenery.tiles)
        for tile in hit_list:
            if movement[1] > 0:
                self.player.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                self.player.top = tile.bottom
                collision_types['top'] = True

        return collision_types

    def react_to(self, event: pygame.event.Event):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.player.moving_right = True
            if event.key == K_LEFT:
                self.player.moving_left = True
            if event.key == K_UP:
                if self.player.air_time < 6:
                    self.jump_sound.play()
                    self.player.y_momentum = -9

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                self.player.moving_right = False
            if event.key == K_LEFT:
                self.player.moving_left = False

    def draw(self, display: pygame.Surface, scroll: Point):
        self.player_view.render(display, self.player, scroll)

TILE_SIZE = 32
WINDOWS_SIZE = (1200, 800)

class Game(object):
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(WINDOWS_SIZE, 0, 32)
        self.display = pygame.Surface((600, 400))
        pygame.display.set_caption('Pygame window')

        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.set_num_channels(64)

        self._init_objects()


    def _init_objects(self) -> List[Controller]:

        player = PlayerModel((50, 50))
        scenery = SceneryModel.from_map_file('map', TILE_SIZE, TILE_SIZE)
        scenery_controller = SceneryController(scenery, ScenaryView())
        player_view = PlayerView()

        player_controller = PlayerController(player, scenery, player_view)

        camera = CameraModel(width=self.display.get_width(), height=self.display.get_height(), following=player)
        camera_controller = CameraController(camera)

        self.controllers: List[Controller] = [camera_controller, scenery_controller, player_controller]
        self.camera = camera_controller

    def _update(self):
        for controller in self.controllers:
            controller.update()

    def _render(self):
        camera_position = self.camera.get_camera_position()
        for controller in self.controllers:
            controller.draw(self.display, camera_position)

    def _process_event(self, event: pygame.event.Event):
        for controller in self.controllers:
            controller.reacto_to(event)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self._update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self._process_event(event)

            surf = pygame.transform.scale(self.display, WINDOWS_SIZE)
            self.screen.blit(surf, (0, 0))
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    Game().run()













