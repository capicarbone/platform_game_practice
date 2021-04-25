
from config import ASSETS_FOLDER
import pygame
from pygame.locals import *
from engine import Controller
from engine.utils import Point
from models import SceneryModel
from views import SceneryView


class SceneryController(Controller):
    def __init__(self, scenery: SceneryModel, view: SceneryView):
        self.scenery = scenery
        self.view = view

        pygame.mixer.music.load(ASSETS_FOLDER + 'music/music.wav')
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