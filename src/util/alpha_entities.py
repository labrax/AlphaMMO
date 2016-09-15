# -*- coding: utf-8 -*-

import time


class Tile:
    def __init__(self):
        self.tile = None
        self.decor_objects = list()
        self.items = list()
        self.entities = set()

    def __iter__(self):
        return self.iter()

    def iter(self):
        if self.tile:
            yield self.tile
        for i in self.decor_objects:
            yield i
        for i in self.items:
            yield i

    def load(self, resource_loader):
        if self.tile:
            self.tile = resource_loader.get_sprite(self.tile[0], self.tile[1], self.tile[2])
        for i in range(len(self.decor_objects)):
            self.decor_objects[i] = resource_loader.get_sprite(self.decor_objects[i][0], self.decor_objects[i][1], self.decor_objects[i][2])
        for i in range(len(self.items)):
            self.items[i] = resource_loader.get_sprite(self.items[i][0], self.items[i][1], self.items[i][2])


class EntityVisual:
    def __init__(self):
        self.skin = 0
        self.hair = 0
        self.helmet = 0
        self.shirt = 0
        self.trousers = 0
        self.boots = 0

        self.shield = 0
        self.weapon = 0

        self.compiled = None

    def update(self):
        #TODO: generate another compiled
        pass


class Entity:
    def __init__(self):
        self.entity_id = -1
        self.speed_pixels = 16

        self.sprite = EntityVisual()
        self.exp = 1

        self.hp = (50, 50)
        self.mp = (0, 0)

        self.attack = 1
        self.defense = 1

        self.pos = (6, 6)
        self.movement = (6, 6)
        self.start_movement = None
        self.player_controlled = False
        self.name = ''
        self.entity_name_surface = None

    def set_movement(self, delta_x, delta_y, immediate=False):
        self.movement = (self.movement[0] + delta_x, self.movement[1] + delta_y)
        if immediate:
            self.start_movement = None
        else:
            self.start_movement = time.time()

    def load(self, resource_loader):
        self.sprite = resource_loader.get_sprite(self.sprite[0], self.sprite[1], self.sprite[2])
