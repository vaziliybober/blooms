from game_view.sprite import Sprite
from game_view.field_view import FieldView
from game_view.images import images
import game_view.colours as colours
import pygame


class BoardView:
	def __init__(self, board, game):
		def mapFields(fields, fieldWidth, fieldHeight):
			self.sprite.setImage(pygame.Surface(self.sprite.rect.size))
			self.sprite.image.fill(colours.WHITE)

			redTerritory = board.getTerritory("red")
			blueTerritory = board.getTerritory("blue")

			for field in fields:
				fieldView = FieldView(field)
				self.fieldViews.append(fieldView)

				fieldView.sprite.rect.center = self.sprite.rect.center

				x = fieldWidth * field.coords.x - int(fieldWidth / 2) * field.coords.y
				y = (-1) * int(fieldHeight * 3 / 4) * field.coords.y
				fieldView.sprite.rect.move_ip(x, y)
				fieldView.draw(self.sprite.image)

				if field in redTerritory:
					territoryImage = Sprite(images.get("red_territory"))
					territoryImage.rect.center = fieldView.sprite.rect.center
					territoryImage.draw(self.sprite.image)
				if field in blueTerritory:
					territoryImage = Sprite(images.get("blue_territory"))
					territoryImage.rect.center = fieldView.sprite.rect.center
					territoryImage.draw(self.sprite.image)

				wholeRestriction = None
				hollowRestriction = None
				if not game.moveIsNotFinished and field.isEmpty():
					wholeRestriction = bool(not game.firstStoneIsValid(field.coords, "whole"))
					hollowRestriction = bool(not game.firstStoneIsValid(field.coords, "hollow"))
				elif game.moveIsNotFinished and field.isEmpty():
					wholeRestriction = bool(not game.secondStoneIsValid(field.coords, "whole"))
					hollowRestriction = bool(not  game.secondStoneIsValid(field.coords, "hollow"))

				restrictionImage = None
				if wholeRestriction and hollowRestriction:
					restrictionImage = Sprite(images.get("field_restriction"))
				elif wholeRestriction:
					restrictionImage = Sprite(images.get("whole_stone_restriction"))
				elif hollowRestriction:
					restrictionImage =  Sprite(images.get("hollow_stone_restriction"))

				if restrictionImage:
					restrictionImage.rect.center= fieldView.sprite.rect.center
					restrictionImage.draw(self.sprite.image)


		self.sprite = Sprite()
		fieldWidth, fieldHeight = images.get("field").get_rect().size
		self.sprite.rect.size = (fieldWidth * (board.size * 2 + 1), fieldHeight + int(fieldHeight * 3 / 4) * (board.size * 2))

		self.fieldViews = []
		mapFields(board.fields.get(), fieldWidth, fieldHeight)

		

	def getFieldByCoords(self, coords):
		possibleFields = []
		for fieldView in self.fieldViews:
			if fieldView.sprite.rect.collidepoint(coords):
				possibleFields.append(fieldView)

		if not possibleFields:
			return None

		def distance(point1, point2):
			return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

		theField = possibleFields[0]
		theDistance = distance(theField.sprite.rect.center, coords)
		for field in possibleFields:
			dist = distance(field.sprite.rect.center, coords)
			if theDistance > dist:
				theField = field
				theDistance = dist

		return theField.field


	def draw(self, surface):
		self.sprite.draw(surface)
		