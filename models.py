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

        top_free = y_position - 1 < 0 or game_map[y_position - 1][x_position] == '0'
        bottom_free = y_position + 1 >= map_height or game_map[y_position + 1][x_position] == '0'
        left_free = x_position - 1 < 0 or game_map[y_position][x_position - 1] == '0'
        right_free = x_position + 1 >= map_width or game_map[y_position][x_position + 1] == '0'

        top_left_free = y_position - 1 >= 0 and x_position - 1 >= 0 and game_map[y_position - 1][x_position - 1] == '0'
        top_right_free = y_position - 1 >= 0 and x_position + 1 < map_width and game_map[y_position - 1][x_position + 1] == '0'
        bottom_right_free = y_position + 1 < map_height and x_position + 1 < map_width and game_map[y_position + 1][
            x_position + 1] == '0'
        bottom_left_free = y_position + 1 < map_height and x_position - 1 >= 0 and game_map[y_position + 1][
            x_position - 1] == '0'

        if bottom_left_free and not bottom_free and not left_free:
            # TODO Add variants

            return '18'

        if bottom_right_free and not bottom_free and not right_free:
            if left_free:
                return '20'

            return '17'

        if top_right_free and not top_free and not right_free:
            if bottom_free:
                return '22'

            return '15'

        if top_left_free and not top_free and not left_free:
            # TODO Add variants

            return '16'


        if left_free and right_free:
            if bottom_free:
                return '13'
            return '14'

        if bottom_free and top_free:
            if right_free:
                return '11'
            if left_free:
                return '12'

            return '10'

        if top_free:
            if right_free:
                return '3'

            if left_free:
                return '4'

            return '2'

        if bottom_free:
            if left_free:
                return '6'
            if right_free:
                return '7'

            return '9'

        if left_free:
            return '5'

        if right_free:
            return '8'

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
