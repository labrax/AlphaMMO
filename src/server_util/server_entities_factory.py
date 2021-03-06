# -*- coding: utf-8 -*-

import random

from util.alpha_entities import Entity, AlphaEffect


class AlphaServerEntitiesFactory:
    """
    Stores information about the initialization of entities
    AlphaServerEntitiesFactory.curr_entity_id is the current entity id
    """
    def __init__(self):
        self.curr_entity_id = 10000

    def _get_entity_id(self):
        """
        An identifier for a new entity
        :return: the identifier
        """
        ret = self.curr_entity_id
        self.curr_entity_id += 1
        return ret

    def create_random(self):
        """
        Create a random entity
        :return: the entity
        """
        entity = Entity()
        entity.sprite = ('roguelikeChar_transparent.png', random.randint(0, 1), random.randint(5, 11))
        entity.entity_id = self._get_entity_id()
        entity.speed_pixels = 16
        return entity

    def create_random_player(self):
        """
        Create a random player entity
        :return: the entity
        """
        entity = self.create_random()
        entity.pos = (8, 8)
        entity.sprite = ('roguelikeChar_transparent.png', random.randint(0, 1), random.randint(5, 11))
        entity.entity_id = self._get_entity_id()
        entity.speed_pixels = 16 * 5
        entity.player_controlled = True
        entity.name = "-"
        print("started at", entity.pos)
        return entity

    def create_random_npc(self):
        """
        Create a random npc
        :return: the entity
        """
        entity = self.create_random()
        entity.pos = (random.randint(2, 10), random.randint(2, 10))
        entity.name = random.choice(['Mark', 'Joe', 'Josh', 'Mary'])
        return entity

    def create_effect(self, pos):
        """
        Create an effect
        :param pos: the position for the effect
        :return: the effect
        """
        effect = AlphaEffect(pos, [('roguelikeChar_transparent.png', 0, 0),
                                   ('roguelikeChar_transparent.png', 0, 1),
                                   ('roguelikeChar_transparent.png', 0, 2),
                                   ('roguelikeChar_transparent.png', 0, 3)], 2, 1)
        return effect
