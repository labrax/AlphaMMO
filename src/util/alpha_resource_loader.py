# -*- coding: utf-8 -*-

import pygame

from util.alpha_defines import ASSETS_DIR, SPRITE_LEN, FONT_FILE, FONT_SIZE
from util.alpha_exceptions import AlphaException


class AlphaSprite(object):
    """
    Stores information for a sprite
    """
    def __init__(self, image=None, file=None):
        """
        Initiates AlphaSprite with a pygame image or a file
        :param image: the surface information
        :param file: the file to load
        """
        if image and file:
            raise AlphaException('Start the image with only one source.')
        self.image = None
        if image:
            self.load_from_memory(image)
        elif file:
            self.load_from_file(file)

    def load_from_memory(self, image):
        """
        Set the image from memory
        :param image: the source image
        :return: nothing
        """
        self.image = image

    def load_from_file(self, file):
        """
        Set the image from file
        :param file: the source file path
        :return: self object
        """
        # http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
        try:
            self.image = pygame.image.load(file)
        except pygame.error:
            print('Cannot load file for sprite:', file)
            raise AlphaException('Cannot load file')
        return self


class AlphaResourceAsset(AlphaSprite):
    """
    Stores information for an asset file
    AlphaResourceAsset.file_sprites is a dict with some preloaded values
    """
    def __init__(self, image=None, file=None):
        super(AlphaResourceAsset, self).__init__(image, file)
        self.file_sprites = dict()

    def get_sprite(self, x, y):
        """
        Get a sprite given a position (considering the SPRITE_LEN constant)
        :param x: the x position
        :param y: the y position
        :return: the sprite
        """
        if (x, y) in self.file_sprites:
            return self.file_sprites[(x, y)]

        source = self.image
        source.set_clip(pygame.Rect(x*(SPRITE_LEN+1), y*(SPRITE_LEN+1), SPRITE_LEN, SPRITE_LEN))
        reply = source.subsurface(source.get_clip())
        self.file_sprites[(x, y)] = reply
        return reply


class AlphaResourceLoader:
    """
    Stores information of the loaded assets, return sprites and font
    AlphaResourceLoader.files_sprites is a dict with assets information (only access using the method)
    AlphaResourceLoader.font is the font loaded (only access using the method)
    """
    def __init__(self):
        self.files_sprites = dict()
        self.font = None

    def get_sprite(self, raw_file, x, y):
        """
        Get a sprite from a given file and position
        :param raw_file: the file path
        :param x: the x position
        :param y: the y position
        :return: the sprite
        """
        file = ASSETS_DIR + raw_file
        if file not in self.files_sprites:
            self.files_sprites[file] = AlphaResourceAsset().load_from_file(file)

        return self.files_sprites[file].get_sprite(x, y)

    def get_font(self, fontfile=ASSETS_DIR + FONT_FILE, fontsize=FONT_SIZE):
        """
        Get a font given a file and size
        :param fontfile: the font file path
        :param fontsize: the font size
        :return: the font
        """
        if not self.font:
            pygame.font.init()
            self.font = pygame.font.Font(fontfile, fontsize)
        return self.font
