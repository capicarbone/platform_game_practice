
import pygame
from config import ASSETS_FOLDER
from models import SceneryModel

class SceneryView(object):
    def __init__(self):
        self.tiles_images = {}
        self.tiles_images['2'] = pygame.image.load(ASSETS_FOLDER + 'tiles/grass.png')
        self.tiles_images['1'] = pygame.image.load(ASSETS_FOLDER + 'tiles/dirt.png')
        self.tiles_images['3'] = pygame.image.load(ASSETS_FOLDER + 'tiles/right_corner.png')
        self.tiles_images['4'] = pygame.image.load(ASSETS_FOLDER + 'tiles/left_corner.png')

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
