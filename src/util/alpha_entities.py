# -*- coding: utf-8 -*-

import time


class AlphaElement:
    def load(self, resource_loader):
        """
        Load the sprites given tuples in (asset file name, X position, Y position) format
        :param resource_loader: the class that load files and retrieve sprites
        :return: nothing
        """
        pass


class Tile(AlphaElement):
    """
    Stores information for a single tile on the game
    Tile.tile is the tile sprite
    Tile.decor_objects are the visual objects on it
    Tile.items are the items on it
    Tile.entities are the entities on it
    Tile.can_walk if the tile is walkable
    """
    def __init__(self):
        self.tile = None
        self.decor_objects = list()
        self.items = list()
        self.entities = set()
        self.can_walk = True

    def __iter__(self):
        """
        Iterator for Tile sprites in the drawing order (first background, later foreground)
        :return: a sprite iterator
        """
        return self.iter()

    def iter(self):
        """
        Generator for Tile sprites
        :return: the sprites
        """
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


class EntityVisual(AlphaElement):
    """
    Stores the information for an entity visual
    EntityVisual.skin
    EntityVisual.hair
    EntityVisual.helmet
    EntityVisual.shirt
    EntityVisual.trousers
    EntityVisual.boots
    EntityVisual.shield
    EntityVisual.weapon
    EntityVisual.compiled
    """
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

    def load(self, resource_loader):
        pass


class Entity(AlphaElement):
    """
    Stores information for an entity in the game
    Entity.entity_id is the identifier
    Entity.speed_pixels is the speed
    Entity.sprite is the entity sprite
    Entity.exp is the entity experience
    Entity.hp is (current health, maximum health)
    Entity.mp is (current mana points, maximum mana points)
    Entity.attack is the attack
    Entity.defense is the defense
    Entity.pos is the position
    Entity.movement is the goal position for a movement
    Entity.start_movement is the time the movement started
    Entity.start_action is the time the action started
    Entity.name is the entity name
    Entity.entity_name_surface is a pre-rendered surface with the name
    """
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
        self.movement = None
        self.start_movement = None
        self.start_action = None
        self.player_controlled = False
        self.name = ''
        self.entity_name_surface = None

    def set_movement(self, delta_x, delta_y, immediate=False):
        """
        Starts the entity movement
        :param delta_x: relative to current position
        :param delta_y: relative to current position
        :param immediate: or not
        :return: nothing
        """
        self.movement = (self.pos[0] + delta_x, self.pos[1] + delta_y)
        if immediate:
            self.start_movement = None
        else:
            self.start_movement = time.time()

    def load(self, resource_loader):
        self.sprite = resource_loader.get_sprite(self.sprite[0], self.sprite[1], self.sprite[2])


class AlphaEffect(AlphaElement):
    """
    Stores information for a visual effect in the game
    AlphaEffect.pos is the position
    AlphaEffect.sprites is a list of sprites
    AlphaEffect.repeats is the amount of repetitions
    AlphaEffect.duration is the duration for the sequence of sprites in the list
    AlphaEffect.first_time is the starting time
    """
    def __init__(self, pos, sprites, repeats, duration):
        self.pos = pos
        self.sprites = sprites
        self.repeats = repeats
        self.duration = duration
        self.first_time = time.time()

    def load(self, resource_loader):
        sprites = list()
        for i in self.sprites:
            sprites.append(resource_loader.get_sprite(i[0], i[1], i[2]))
        self.sprites = sprites

    def get_sprite(self):
        """
        Get the current sprite in the effect animation
        :return: None if the effect is over or the sprite if available
        """
        curr_time = time.time()
        if curr_time - self.first_time > self.duration * self.repeats:
            return None
        else:
            time_at_current_loop = (curr_time - self.first_time) % self.duration
            curr = int(time_at_current_loop/self.duration * len(self.sprites))
            return self.sprites[curr]
