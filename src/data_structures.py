# -*- coding: utf-8 -*-


class Tile:
    def __init__(self):
        self.tile = None
        self.decor_objects = list()
        self.items = list()
        self.characters = list()

    def __iter__(self):
        return self.iter()

    def iter(self):
        if self.tile:
            yield self.tile
        for i in self.decor_objects:
            yield i
        for i in self.items:
            yield i
        for i in self.characters:
            yield i