# -*- coding: utf-8 -*-

import pygame
from pygame.locals import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION


class ClientInput:
    def __init__(self):
        self.channel = None

    def handle(self, event):
        if event.type == KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.channel.push(['KEY', 'LEFT'])
            elif event.key == pygame.K_RIGHT:
                self.channel.push(['KEY', 'RIGHT'])
            elif event.key == pygame.K_UP:
                self.channel.push(['KEY', 'UP'])
            elif event.key == pygame.K_DOWN:
                self.channel.push(['KEY', 'DOWN'])
            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.channel.push(['KEY', 'ENTER'])
        elif event.type == KEYUP:
            pass
        elif event.type == MOUSEBUTTONDOWN:
            pass
        elif event.type == MOUSEBUTTONUP:
            pass
        elif event.type == MOUSEMOTION:
            pass
