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
        self.pixels_speed = 16
        self.max_hp = 100
        self.hp = 100
        self.max_mp = 50
        self.mp = 50
        self.attack = 1
        self.defense = 1
        self.pos_x = 6
        self.pos_y = 6
        self.sprite = None
