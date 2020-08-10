from view.sprite import Sprite
from view.images import images
from game.player import player1, player2
from game.stone import type1, type2


class Stone:
	def __init__(self, stone):
		if stone.type == type1:
			if stone.player == player1:
				imageName = "stone11"
			if stone.player == player2:
				imageName = "stone12"
		if stone.type == type2:
			if stone.player == player1:
				imageName = "stone21"
			if stone.player == player2:
				imageName = "stone22"

		self.sprite = Sprite(images.get(imageName))

	def draw(self, surface):
		self.sprite.draw(surface)