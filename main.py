import random
from typing import Dict

import sys
from engine import Controller
from pygame.locals import *
from models import *
from views import *
from controllers import *

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
        scenery_controller = SceneryController(scenery, SceneryView(), False)
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
            controller.react_to(event)

    def run(self):
        clock = pygame.time.Clock()
        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self._process_event(event)

            self._update()
            self._render()

            surf = pygame.transform.scale(self.display, WINDOWS_SIZE)
            self.screen.blit(surf, (0, 0))
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    Game().run()













