# -*- coding: utf-8 -*-

from client_entities import Entity as ServerEntity


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


class ServerTile:
    def __init__(self):
        self.tile = None
        self.decor_objects = list()
        self.items = list()
        self.entities = list()

    def __iter__(self):
        return self.iter()

    def iter(self):
        if self.tile:
            yield self.tile
        for i in self.decor_objects:
            yield i
        for i in self.items:
            yield i
