
import pygame
from engine.utils import Point

# TODO make abstract

class Controller(object):
    def react_to(self, event: pygame.event.Event):
        pass

    def update(self):
        pass

    def draw(self, display: pygame.Surface, scroll: Point):
        pass