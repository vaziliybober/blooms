from game_view.stone_view import StoneView
from game_view.sprite import Sprite
from game_view.images import images


class FieldView:
	def __init__(self, field):
		self.sprite = Sprite(images.get("field"))
		self.field = field

		self.stoneView = None
		if not field.isEmpty():
			self.stoneView = StoneView(field.stone)

	def draw(self, surface):
		self.sprite.draw(surface)

		if self.stoneView:
			self.stoneView.sprite.rect.center = self.sprite.rect.center
			self.stoneView.draw(surface)



