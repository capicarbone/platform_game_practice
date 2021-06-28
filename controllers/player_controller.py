from typing import List, Dict
import random
import pygame
from pygame.locals import *
from config import ASSETS_FOLDER
from engine import Controller
from engine.utils import collision_test, Point
from models import PlayerModel, SceneryModel, PlayerActions
from views import PlayerView

# TODO move to a dict of actions : frames durations
ATTACK_FRAMES = 25

class PlayerController(Controller):

    def __init__(self, player: PlayerModel, scenery: SceneryModel, view: PlayerView):
        self.player = player
        self.view = view
        self.scenery = scenery
        self.grass_sound_timer = 0
        self._load_sounds()

    def _load_sounds(self):
        self.jump_sound = pygame.mixer.Sound(ASSETS_FOLDER + 'sounds/jump.wav')
        self.grass_sounds = [pygame.mixer.Sound(ASSETS_FOLDER + 'sounds/grass_0.wav'),
                             pygame.mixer.Sound(ASSETS_FOLDER + 'sounds/grass_1.wav')]
        self.grass_sounds[0].set_volume(0.2)
        self.grass_sounds[1].set_volume(0.2)

    def update(self):

        if self.grass_sound_timer > 0:
            self.grass_sound_timer -= 1

        movement = [0, 0]

        if self.player.action == PlayerActions.ATTACK and self.player.action_frame != ATTACK_FRAMES:
            self.player.action_frame += 1
        else:

            if self.player.moving_right:
                movement[0] += 4
            if self.player.moving_left:
                movement[0] -= 4
            movement[1] += self.player.y_momentum
            self.player.y_momentum += 0.4
            if self.player.y_momentum > 9:
                self.player.y_momentum = 9

        collisions = self._move(movement)

        if collisions['bottom']:
            """
            Yes, our player will be constantly "falling" but we rely on
            collissions detection to know if we are actually falling.
            """
            self.player.y_momentum = 0.4
            self.player.air_time = 0
            if movement[0] != 0:
                if self.grass_sound_timer == 0:
                    self.grass_sound_timer = 30
                    random.choice(self.grass_sounds).play()
        else:
            self.player.air_time += 1


        if movement[0] > 0:
            self.player.action = PlayerActions.WALK
            self.player.front_to_right = True

        if movement[0] < 0:
            self.player.action = PlayerActions.WALK
            self.player.front_to_right = False

        if movement[0] == 0 and collisions['bottom']:
            self.player.action = PlayerActions.IDLE

        if movement[1] < 0:
            self.player.action = PlayerActions.JUMP

        if movement[1] >= 0 and not collisions['bottom'] and self.player.action != PlayerActions.ATTACK:
            self.player.action = PlayerActions.FALL

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

        # We should take small y movements has potential collisions
        y_movement = 1 if 0 < movement[1] < 1 else movement[1]
        self.player.y += y_movement
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
            if event.key == K_x:
                if self.player.action is not PlayerActions.JUMP and self.player.action is not PlayerActions.FALL:
                    self.player.start_attack()
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
        self.view.render(display, self.player, scroll)
