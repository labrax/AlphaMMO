# -*- coding: utf-8 -*-

import time

from util.alpha_entities import Tile, Entity
from util.alpha_defines import GRID_MEMORY_SIZE


class AlphaServerMap:
    def __init__(self):
        self.map_dimension = (16, 16)
        self.tiled_memory = None

        self.all_entities = dict()

    def start(self):
        # dummy map
        self.tiled_memory = [[Tile() for _2 in range(self.map_dimension[0])] for _ in range(self.map_dimension[1])]
        for i in range(self.map_dimension[1]):
            for j in range(self.map_dimension[0]):
                if i % 3 == 0 and j % 5 == 0:
                    self.tiled_memory[i][j].tile = ('roguelikeDungeon_transparent.png', 17, 15)
                elif i % 4 == 0 and j % 7 == 0:
                    self.tiled_memory[i][j].tile = ('roguelikeDungeon_transparent.png', 20, 15)
                else:
                    self.tiled_memory[i][j].tile = ('roguelikeDungeon_transparent.png', 16, 15)
                if i % 9 == 0 and j % 3 == 0:
                    self.tiled_memory[i][j].decor_objects.append(
                        ('roguelikeDungeon_transparent.png', 2, 2))
                if i % 7 == 0 and j % 2 == 0:
                    self.tiled_memory[i][j].decor_objects.append(
                        ('roguelikeDungeon_transparent.png', 0, 2))
        self.tiled_memory[6][6].decor_objects.append(('roguelikeDungeon_transparent.png', 0, 0))

        p1 = Entity()
        p1.pos = (5, 6)
        p1.sprite = ('roguelikeChar_transparent.png', 1, 9)
        p1.entity_id = 2
        p1.speed_pixels = 8
        p1.movement = (4, 6)
        p1.start_movement = time.time()
        p1.name = 'AaaN'
        self.tiled_memory[6][5].entities.append(p1)

        p2 = Entity()
        p2.pos = (2, 2)
        p2.sprite = ('roguelikeChar_transparent.png', 0, 7)
        p2.entity_id = 3
        p2.speed_pixels = 4
        p2.movement = (1, 1)
        p2.start_movement = time.time()
        p2.name = 'Bbbhashashahsa'
        self.tiled_memory[2][2].entities.append(p2)

        for i in [p1, p2]:
            self.all_entities[i.entity_id] = i

    def get_entities(self, curr_entity):
        curr_entity = self.all_entities[curr_entity]
        ret_entities = list()
        for j in range(curr_entity.pos[1] - int(GRID_MEMORY_SIZE[1] / 2),
                       curr_entity.pos[1] + int(GRID_MEMORY_SIZE[1] / 2)):
            for i in range(curr_entity.pos[0] - int(GRID_MEMORY_SIZE[0] / 2),
                           curr_entity.pos[0] + int(GRID_MEMORY_SIZE[0] / 2)):
                if 0 <= i < GRID_MEMORY_SIZE[0] and 0 <= j < GRID_MEMORY_SIZE[1]:
                    for elem in self.tiled_memory[j][i].entities:
                        if elem is not curr_entity:
                            ret_entities.append(elem)
        return ret_entities
