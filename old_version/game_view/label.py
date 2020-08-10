import pygame
from game_view.sprite import Sprite
from game_view.images import images
from game_view.measurer import measurer
import game_view.fonts as fonts
import game_view.colours as colours

class Label:
	def __init__(self, text):
		self.sprite = Sprite(images.get("label"))
		self.font = fonts.default
		self.textSize = measurer.get("default text size")
		self.textColour = colours.BLACK
		self.bold = False
		self.italic = False

		self.setText(text)

	def setText(self, text):
		self.text = text
		self.textSprite = Sprite(pygame.font.SysFont(self.font, self.textSize, self.bold, self.italic).render(text, True, self.textColour))

	def setFont(self, font):
		self.font = font
		self.setText(self.text)

	def setTextSize(self, textSize):
		self.textSize = textSize
		self.setText(self.text)

	def setTextColour(self, textColour):
		self.textColour = textColour
		self.setText(self.text)

	def setBold(self, bold):
		self.bold = bold
		self.setText(self.text)

	def setItalic(self, italic):
		self.italic = italic
		self.setText(self.text)

	def draw(self, surface):
		self.textSprite.rect.center = self.sprite.rect.center
		self.sprite.draw(surface)
		self.textSprite.draw(surface)