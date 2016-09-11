# -*- coding: utf-8 -*-

import pygame

from util.alpha_defines import ASSETS_DIR, SPRITE_LEN, FONT_FILE, FONT_SIZE
from util.game_exceptions import AlphaException


class AlphaSprite:
    def __init__(self, image=None, file=None):
        if image and file:
            raise AlphaException('Start the image with only one source.')
        self.image = None
        if image:
            self.load_from_memory(image)
        elif file:
            self.load_from_file(file)

    def load_from_memory(self, image):
        self.image = image


class AlphaResourceAsset(AlphaSprite):
    def __init__(self, image=None, file=None):
        super(AlphaResourceAsset, self).__init__(image, file)
        self.file_sprites = dict()

    def get_sprite(self, x, y):
        if (x, y) in self.file_sprites:
            return self.file_sprites[(x, y)]

        source = self.image
        source.set_clip(pygame.Rect(x*(SPRITE_LEN+1), y*(SPRITE_LEN+1), SPRITE_LEN, SPRITE_LEN))
        reply = source.subsurface(source.get_clip())
        self.file_sprites[(x, y)] = reply
        return reply

    def load_from_file(self, file):
        # http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
        try:
            self.image = pygame.image.load(file)
        except pygame.error:
            print('Cannot load file for sprite:', file)
            raise AlphaException('Cannot load file')
        return self


class AlphaResourceLoader:
    def __init__(self):
        self.files_sprites = dict()
        self.font = None

    def get_sprite(self, raw_file, x, y):
        file = ASSETS_DIR + raw_file
        if file not in self.files_sprites:
            self.files_sprites[file] = AlphaResourceAsset().load_from_file(file)

        return self.files_sprites[file].get_sprite(x, y)

    def get_font(self):
        #return pygame.font.Font(None, FONT_SIZE)
        if not self.font:
            pygame.font.init()
            self.font = pygame.font.Font(ASSETS_DIR + FONT_FILE, FONT_SIZE)
        return self.font
