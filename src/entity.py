# -*- coding: utf-8 -*-

import time


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
    def __init__(self, visual_element, name, handler):
        """
        initiates an entity for the game
        :param visual_element: the visual part of the entity
        :param name: the name of it (or identifier)
        :param handler: the tasklet that will run it
        """
        self.visual_element = visual_element
        self.name = name
        self.handler = handler


class Map(Entity):
    def __init__(self):
        super(Map, self).__init__()