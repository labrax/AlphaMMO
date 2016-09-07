# -*- coding: utf-8 -*-

import time
from data_structures import Tile


class VisualElement:
    def __init__(self, sprites, animation_time):
        """
        initiates a visual element for an entity
        :param sprites: a list or a single sprite
        :param animation_time: the duration of an animation (if it is one)
        """
        self._sprites = sprites
        self.last_draw = None
        self.animation_time = animation_time

    def get_sprite(self):
        if type(self._sprites) is not list:
            return self._sprites

        if not self.last_draw:
            return self._sprites[0]
        else:
            self.last_draw = time.time()
            return self._sprites[int((time.time() - self.last_draw)*len(self._sprites)/self.animation_time)]


class Entity:
    def __init__(self):
        self.speed_pixels = 16
        self.hp = (100, 100)
        self.mp = (50, 50)
        self.attack = 1
        self.defense = 1
        self.pos = (6, 6)
        self.movement = (6, 6)
        self.sprite = None
        self.start_movement = None

    def set_movement(self, delta_x, delta_y, immediate=False):
        self.movement = (self.movement[0] + delta_x, self.movement[1] + delta_y)
        if immediate:
            self.start_movement = None
        else:
            self.start_movement = time.time()
