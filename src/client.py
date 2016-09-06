#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import pygame


class GameScreen:
	def __init__(self):
		self.screen = pygame.display.set_mode((600, 480))
		pygame.display.flip()

	def run(self):
		running = True
		while running:
			event = pygame.event.wait()
			if event.type == pygame.QUIT:
				running = False
		pygame.quit()


if __name__ == '__main__':
	gs = GameScreen()
	gs.run()


