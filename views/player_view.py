from typing import Dict

from config import ASSETS_FOLDER
import pygame
from pygame import Surface
from engine.utils import Point
from models import PlayerModel, PlayerActions


class PlayerView(object):
    _DEFAULT_PLAYER_HEIGHT = 32
    _DEFAULT_PLAYER_WIDTH = 26

    def __init__(self):
        self.displaying_action = PlayerActions.IDLE
        self.player_frame = 0
        self.animation_database = {}
        self.animation_frames: Dict[str, Surface] = {}
        self.animation_database[PlayerActions.IDLE] = self._load_animation(ASSETS_FOLDER + 'characters/player/idle',
                                                                           [10, 10, 10, 10])
        self.animation_database[PlayerActions.WALK] = self._load_animation(ASSETS_FOLDER + 'characters/player/walk',
                                                                           [7, 7, 7, 7, 7, 7])
        self.animation_database[PlayerActions.JUMP] = self._load_animation(ASSETS_FOLDER + 'characters/player/jump',
                                                                           [5, 5, 7, 7])
        self.animation_database[PlayerActions.FALL] = self._load_animation(ASSETS_FOLDER + 'characters/player/fall',
                                                                           [7])
        self.animation_database[PlayerActions.ATTACK] = self._load_animation(ASSETS_FOLDER + 'characters/player/attack',
                                                                             [int(25 / 6)] * 6)

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
        if self.displaying_action != new_value:
            self.displaying_action = new_value
            self.player_frame = 0

    def render(self, display: pygame.Surface, player: PlayerModel, scroll: Point):
        self._change_action(player.action)
        self.player_frame += 1

        if self.player_frame >= len(self.animation_database[player.action]):
            self.player_frame = 0

        player_img_id = self.animation_database[player.action][self.player_frame]
        player_image = self.animation_frames[player_img_id]

        # Sprites like those for jump action have height greater than 32, so we adjust wht height
        y_adjustment = player_image.get_height() - self._DEFAULT_PLAYER_HEIGHT
        x_adjustment = 0
        if not player.front_to_right:
            x_adjustment = player_image.get_width() - self._DEFAULT_PLAYER_WIDTH

        display.blit(pygame.transform.flip(player_image, not player.front_to_right, False),
                     (player.x - scroll[0] - x_adjustment, player.y - scroll[1] - y_adjustment))
