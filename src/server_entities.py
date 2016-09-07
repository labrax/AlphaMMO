# -*- coding: utf-8 -*-


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