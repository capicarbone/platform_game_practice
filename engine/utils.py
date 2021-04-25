
from typing import List
from pygame import Rect
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

def collision_test(rect: Rect, tiles: List[Rect]):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list
