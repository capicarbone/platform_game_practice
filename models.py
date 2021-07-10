from typing import Tuple, List

import pygame
from enum import Enum, auto


class PlayerActions(Enum):
    IDLE = auto()
    WALK = auto()
    JUMP = auto()
    FALL = auto()
    ATTACK = auto()


class PlayerModel(pygame.Rect):
    def __init__(self, star_position: Tuple[int, int]):
        super().__init__(star_position[0], star_position[1], 26, 32)
        self.y_momentum = 0
        self.moving_right = False
        self.moving_left = False
        self.air_time = 0
        self.action = PlayerActions.IDLE
        self.front_to_right = True
        self.action_frame = 0

    def start_attack(self):
        self.action_frame = 1
        self.action = PlayerActions.ATTACK


class Tile(pygame.Rect):
    def __init__(self, left, top, width, height, type: str):
        super(Tile, self).__init__(left, top, width, height)
        self.type = type


class SceneryModel(object):
    def __init__(self, tiles: List[Tile]):
        self.tiles = tiles

    @staticmethod
    def _get_tile_type(game_map, x_position: int, y_position: int):
        map_height = len(game_map)
        map_width = len(game_map[0])

        top_free = y_position - 1 >= 0 and game_map[y_position - 1][x_position] == '0'
        bottom_free = y_position + 1 < map_height and game_map[y_position + 1][x_position] == '0'
        left_free = x_position - 1 >= 0 and game_map[y_position][x_position - 1] == '0'
        right_free = x_position + 1 < map_width and game_map[y_position][x_position + 1] == '0'

        if top_free:
            if right_free:
                return '3'

            if left_free:
                return '4'

            return '2'

        return '1'


    @staticmethod
    def from_map_file(path: str, tile_width: int, tile_height: int):
        f = open(path + '.txt', 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        game_map = []

        for row in data:
            # avoiding empty linesa
            if len(row) > 1:
                game_map.append(list(row))

        tiles: List[Tile] = []
        for y in range(len(game_map)):
            for x in range(len(game_map[y])):
                if game_map[y][x] != '0':
                    tiles.append(Tile(x * tile_width, y * tile_height, tile_width, tile_height,
                                      SceneryModel._get_tile_type(game_map, x, y)))

        return SceneryModel(tiles)


class CameraModel(object):
    def __init__(self, width: int, height: int, following: pygame.Rect):
        self.x_offset = 0
        self.y_offset = 0
        self.width = width
        self.height = height
        self.following = following
