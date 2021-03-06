# -*- coding: utf-8 -*-


from util.alpha_entities import Tile
from util.alpha_defines import GRID_MEMORY_SIZE, GRID_MEMORY_SIZE as CLIENT_GRID_MEMORY_SIZE
from server_util.alpha_server_defines import PLAYER_PASS_THROUGH_OTHERS


class AlphaServerMap:
    """
    The information about the map: Tiles, Entities
    AlphaServerMap.map_dimension are the dimensions (width, height)
    AlphaServerMap.tiled_memory is the map loaded (list of list of Tile)
    AlphaServerMap.all_entities is the relation of all entities (dict)
    """
    def __init__(self):
        self.map_dimension = (128, 20)
        self.tiled_memory = None
        self.all_entities = dict()

    def start(self):
        """
        Loads the map using random values
        :return: nothing
        """
        # dummy map
        self.tiled_memory = [[Tile() for _2 in range(self.map_dimension[0])] for _ in range(self.map_dimension[1])]
        for i in range(self.map_dimension[1]):
            for j in range(self.map_dimension[0]):
                if (i == 0 or i == self.map_dimension[1] - 1) or (j == 0 or j == self.map_dimension[0] - 1):
                    self.tiled_memory[i][j].tile = ('roguelikeDungeon_transparent.png', 17, 17)
                elif i % 3 == 0 and j % 5 == 0:
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
        self.tiled_memory[8][8].decor_objects.append(('roguelikeDungeon_transparent.png', 0, 0))
        self.tiled_memory[8][8].can_walk = False

    def get_nearby_entities(self, curr_entity):
        """
        Get the entities near one in a bounding box around a central entity (that isn't returned)
        :param curr_entity: the central entity
        :return: a list of entities
        """
        curr_entity = self.all_entities[curr_entity]
        ret_entities = list()
        for j in range(curr_entity.pos[1] - int(GRID_MEMORY_SIZE[1] / 2),
                       curr_entity.pos[1] + int(GRID_MEMORY_SIZE[1] / 2)):
            for i in range(curr_entity.pos[0] - int(GRID_MEMORY_SIZE[0] / 2),
                           curr_entity.pos[0] + int(GRID_MEMORY_SIZE[0] / 2)):
                if self.is_valid((i, j)):
                    for elem in self.tiled_memory[j][i].entities:
                        if elem is not curr_entity:
                            ret_entities.append(elem)
        return ret_entities

    def get_entity(self, entity):
        """
        Return the entity given an identifier
        :param entity: the identifier
        :return: an entity
        """
        return self.all_entities.get(entity, None)

    def set_entity(self, entity):
        """
        Set the information for an entity in the map memory
        :param entity: the entity
        :return: nothing
        """
        self.all_entities[entity.entity_id] = entity
        self.tiled_memory[entity.pos[1]][entity.pos[0]].entities.add(entity)

    def remove_entity(self, entity):
        """
        Remove an entity in the map information, in the Tile and the entities relation
        :param entity: the entity
        :return: nothing
        """
        entity = self.all_entities.pop(entity.entity_id)
        self.tiled_memory[entity.pos[1]][entity.pos[0]].entities.remove(entity)

    def prepare_map(self, player_x, player_y):
        """
        This method returns tiles in a bounding box around a central location
        :param player_x: the x position
        :param player_y: the y position
        :return: a list of list with Tiles
        """
        ret = [[Tile() for _2 in range(CLIENT_GRID_MEMORY_SIZE[0])] for _ in range(CLIENT_GRID_MEMORY_SIZE[1])]
        for j in range(player_y - int(CLIENT_GRID_MEMORY_SIZE[1] / 2),
                       player_y + int(CLIENT_GRID_MEMORY_SIZE[1] / 2)):
            for i in range(player_x - int(CLIENT_GRID_MEMORY_SIZE[0] / 2),
                           player_x + int(CLIENT_GRID_MEMORY_SIZE[0] / 2)):
                if self.is_valid((i, j)):
                    ret[j - (player_y - int(CLIENT_GRID_MEMORY_SIZE[1] / 2))][
                        i - int(player_x - int(CLIENT_GRID_MEMORY_SIZE[0] / 2))] = \
                        self.tiled_memory[j][i]
        return ret

    def is_valid(self, pos):
        """
        Check if a position is inside the map memory and thus valid
        :param pos: the position (X, Y)
        :return: True or False
        """
        if 0 <= pos[0] < self.map_dimension[0] and 0 <= pos[1] < self.map_dimension[1]:
            return True
        return False

    def is_valid_movement(self, pos):
        """
        Check if the position is valid to walk
        :param pos: the position (X, Y)
        :return: True or False
        """
        if self.is_valid(pos)\
                and (PLAYER_PASS_THROUGH_OTHERS or len(self.tiled_memory[pos[1]][pos[0]].entities) == 0) \
                and self.tiled_memory[pos[1]][pos[0]].can_walk:
            return True
        return False

    def move_entity(self, entity, source, target):
        self.tiled_memory[source[1]][source[0]].entities.remove(entity)
        self.tiled_memory[target[1]][target[0]].entities.add(entity)
