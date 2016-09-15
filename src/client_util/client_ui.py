# -*- coding: utf-8 -*-

import pygame
from util.alpha_defines import gray
from util.alpha_resource_loader import AlphaResourceLoader

FONT_COLOR = (180, 180, 180)
WHITE_BORDER = (240, 240, 240)
INTERNAL_COLOR = gray
WINDOW_FONT = AlphaResourceLoader().get_font(fontsize=24)

LABEL_BACKGROUND = (200, 200, 200)
LABEL_FONT = AlphaResourceLoader().get_font(fontsize=24)

EDITBOX_COLOR = (160, 160, 160)
BUTTON_BORDER = (230, 230, 230)


class AlphaGameUI:
    curr_id = 1

    @classmethod
    def get_id(cls):
        ret = cls.curr_id
        cls.curr_id += 1
        return ret

    def __init__(self, pos, size):
        self.id = AlphaGameUI.get_id()
        self.pos = pos
        self.size = size
        self.surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        self.visible = False

    def render(self, dest):
        dest.blit(self.surface, self.pos)

    def update(self):
        pass


class AlphaWindow(AlphaGameUI):
    def __init__(self, pos, size, title_name):
        super(AlphaWindow, self).__init__(pos, size)
        self.title_name = title_name
        self.components = dict()
        self.update()

    def update(self):
        self.surface.fill(INTERNAL_COLOR)
        pygame.draw.rect(self.surface, WHITE_BORDER, pygame.Rect((1, 1), (self.size[0] - 2, self.size[1] - 2)), 2)

        title_surface = WINDOW_FONT.render(self.title_name, 1, FONT_COLOR)

        self.surface.blit(title_surface, ((self.size[0] - title_surface.get_width()) / 2, 3))
        pygame.draw.rect(self.surface, WHITE_BORDER, pygame.Rect((1, title_surface.get_height() + 2), (self.size[0] - 1, self.size[1] - 1 - title_surface.get_height())), 1)

        for i in self.components.values():
            i.update()
            i.render(self.surface)

    def add_component(self, component):
        # (3, 29) is a good position after the screen title
        if type(component) == list:
            for i in component:
                self.components[i.id] = i
        else:
            self.components[component.id] = component


class AlphaLabel(AlphaGameUI):
    def __init__(self, pos, size, text):
        super(AlphaLabel, self).__init__(pos, size)
        self.text = text
        self.update()

    def update(self):
        font_surface = LABEL_FONT.render(self.text, 1, FONT_COLOR)
        self.surface.blit(font_surface, (2, 2))


class AlphaEditBox(AlphaLabel):
    def __init__(self, pos, size, text):
        super(AlphaEditBox, self).__init__(pos, size, text)
        self.update()

    def update(self):
        self.surface.fill(LABEL_BACKGROUND)
        font_surface = LABEL_FONT.render(self.text, 1, EDITBOX_COLOR)
        self.surface.blit(font_surface, (2, 2))

    def notify(self, event):
        # todo: add text
        pass


class AlphaButton(AlphaLabel):
    def __init__(self, pos, size, text, callback, callback_args=None):
        super(AlphaButton, self).__init__(pos, size, text)
        self.callback = callback
        self.callback_args = callback_args

    def update(self):
        font_surface = LABEL_FONT.render(self.text, 1, FONT_COLOR)
        pygame.draw.rect(self.surface, BUTTON_BORDER, pygame.Rect((1, 1), (self.size[0] - 1, self.size[1] - 1)), 1)
        self.surface.blit(font_surface, ((self.size[0] - font_surface.get_width()) / 2, (self.size[1] - font_surface.get_height()) / 2))

    def notify(self, event):
        # todo: check if is return/enter/space/button click in the button area
        self.callback(*self.callback_args)
