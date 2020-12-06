from game_view.sprite import Sprite
from game_view.images import images


class StoneView:
	def __init__(self, stone):
		imageName = "{}_{}_stone".format(stone.colour, stone.type)
		self.sprite = Sprite(images.get(imageName))

	def draw(self, surface):
		self.sprite.draw(surface)