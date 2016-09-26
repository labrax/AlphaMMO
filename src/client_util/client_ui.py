# -*- coding: utf-8 -*-

import pygame
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, KMOD_SHIFT, KMOD_CTRL

from client_util.client_ui_defines import FONT_COLOR, WHITE_BORDER, INTERNAL_COLOR, WINDOW_FONT, LABEL_BACKGROUND, \
    LABEL_FONT, EDITBOX_COLOR, BUTTON_BORDER
from client_util.keys import keys, keys_special


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

    def notify(self, event):
        pass


class AlphaWindow(AlphaGameUI):
    def __init__(self, pos, size, title_name):
        super(AlphaWindow, self).__init__(pos, size)
        self.title_name = title_name
        self.components = dict()
        self.selected = None
        self.enter = None
        self.escape = None
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
                if not self.selected and (isinstance(i, AlphaButton) or isinstance(i, AlphaEditBox)):
                    self.selected = i
                self.components[i.id] = i
        else:
            if not self.selected and (isinstance(component, AlphaButton) or isinstance(component, AlphaEditBox)):
                self.selected = component
            self.components[component.id] = component

    def notify(self, event):
        if event.type == KEYDOWN:
            if event.key in keys_special:
                obj = keys_special[event.key][1]
                if obj in ['return', 'enter', 'keypad enter']:
                    if self.enter:
                        return self.enter.notify(event)
                elif obj in ['escape']:
                    if self.escape:
                        return self.escape.notify(event)
                elif obj == 'tab':
                    rel = [i for i in self.components.values()]
                    for i in range(len(rel)):
                        if rel[i] == self.selected:
                            if pygame.key.get_mods() & KMOD_SHIFT:
                                if i == 0:
                                    self.selected = rel[len(rel) - 1]
                                else:
                                    self.selected = rel[i - 1]
                            else:
                                if i + 1 == len(rel):
                                    self.selected = rel[0]
                                    return True
                                else:
                                    self.selected = rel[i + 1]
                                    return True
            if self.selected:
                return self.selected.notify(event)
        if event.type == MOUSEBUTTONDOWN:
            event_x, event_y = pygame.mouse.get_pos()
            for i in self.components.values():
                if i.pos[0] <= event_x - self.pos[0] <= i.pos[0] + i.size[0] and i.pos[1] <= event_y - self.pos[1] <= i.pos[1] + i.size[1]:
                    self.selected = i
                    i.notify(event)
                    return True


class AlphaLabel(AlphaGameUI):
    def __init__(self, pos, size, text):
        super(AlphaLabel, self).__init__(pos, size)
        self.text = text
        self.update()

    def update(self):
        font_surface = LABEL_FONT.render(self.text, 1, FONT_COLOR)
        self.surface.blit(font_surface, (2, 2))


class AlphaEditBox(AlphaLabel):
    def __init__(self, pos, size, text, password=False):
        self.password = password
        super(AlphaEditBox, self).__init__(pos, size, text)

    def update(self):
        self.surface.fill(LABEL_BACKGROUND)
        if self.password:
            font_surface = LABEL_FONT.render('*' * len(self.text), 1, EDITBOX_COLOR)
        else:
            font_surface = LABEL_FONT.render(self.text, 1, EDITBOX_COLOR)
        self.surface.blit(font_surface, (2, 2))

    def notify(self, event):
        if event.type == KEYDOWN:
            if pygame.key.get_mods() & KMOD_SHIFT and event.key in [pygame.K_0, pygame.K_1, pygame.K_2,
                                                                    pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                                                                    pygame.K_7, pygame.K_8, pygame.K_9]:
                if event.key == pygame.K_2:
                    self.text += '@'
                    return True
            elif event.key in keys_special:
                obj = keys_special[event.key][1]
                if obj in ['backspace'] and len(self.text) > 0:
                    self.text = self.text[:-1]
                    return True
            elif event.key in keys:
                obj = keys[event.key][0]
                if obj == 'u' and pygame.key.get_mods() & KMOD_CTRL:
                    self.text = ''
                else:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        obj = obj.upper()
                    self.text += obj
                return True


class AlphaButton(AlphaLabel):
    def __init__(self, pos, size, text, callback, callback_args=None):
        if not callback_args:
            self.callback_args = ()
        else:
            self.callback_args = callback_args
        self.callback = callback
        super(AlphaButton, self).__init__(pos, size, text)

    def update(self):
        font_surface = LABEL_FONT.render(self.text, 1, FONT_COLOR)
        pygame.draw.rect(self.surface, BUTTON_BORDER, pygame.Rect((1, 1), (self.size[0] - 1, self.size[1] - 1)), 1)
        self.surface.blit(font_surface, ((self.size[0] - font_surface.get_width()) / 2, (self.size[1] - font_surface.get_height()) / 2))

    def notify(self, event):
        # todo: check if is return/enter/space/button click in the button area
        self.callback(*self.callback_args)
