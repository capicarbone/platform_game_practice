
from config import ASSETS_FOLDER
import pygame
from engine.utils import Point
from models import PlayerModel

class PlayerView(object):
    def __init__(self):
        self.player_action = 'idle'
        self.player_frame = 0
        self.animation_database = {}
        self.animation_frames = {}
        self.animation_database['idle'] = self._load_animation(ASSETS_FOLDER + 'characters/player/idle', [10, 10, 10, 10])
        self.animation_database['walk'] = self._load_animation(ASSETS_FOLDER + 'characters/player/walk', [7, 7, 7, 7, 7, 7])

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

        if self.player_frame >= len(self.animation_database[player.action]):
            self.player_frame = 0

        player_img_id = self.animation_database[player.action][self.player_frame]
        player_image = self.animation_frames[player_img_id]
        display.blit(pygame.transform.flip(player_image, not player.front_to_right, False),
                     (player.x - scroll[0], player.y - scroll[1]))