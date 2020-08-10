import pygame
import sys

import game.stone as stone
import game.player as player
import view.stone

s = stone.get(stone.type2, player.player2)
sv = view.stone.Stone(s)

screen = pygame.display.set_mode((800, 400))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	sv.draw(screen)

	pygame.display.flip()

print(s)