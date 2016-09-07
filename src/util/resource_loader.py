# -*- coding: utf-8 -*-

import pygame

from game_exceptions import Alpha_Exception
from alpha_defines import ASSETS_DIR, SPRITE_LEN


class AlphaSprite:
    def __init__(self, image=None, file=None):
        if image and file:
            raise Alpha_Exception('Start the image with only one source.')
        self.image = None
        if image:
            self.load_from_memory(image)
        elif file:
            self.load_from_file(file)

    def load_from_memory(self, image):
        self.image = image

    def load_from_file(self, file):
        # http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
        try:
            self.image = pygame.image.load(file)
        except pygame.error as message:
            print('Cannot load file for sprite:', file)
            raise Alpha_Exception('Cannot load file')
        return self


class AlphaResourceLoader:
    def __init__(self):
        self.files_sprites = dict()

    def get_sprite(self, raw_file, x, y):
        file = ASSETS_DIR + raw_file
        if file not in self.files_sprites:
            self.files_sprites[file] = AlphaSprite().load_from_file(file)
        source = self.files_sprites[file].image
        source.set_clip(pygame.Rect(x*(SPRITE_LEN+1), y*(SPRITE_LEN+1), SPRITE_LEN, SPRITE_LEN))
        return source.subsurface(source.get_clip())
