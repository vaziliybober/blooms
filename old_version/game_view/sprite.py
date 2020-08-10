import pygame

class Sprite:
	def __init__(self, image=None, rect=None):
		self.images = {}

		self.rect = rect if rect else pygame.Rect(0, 0, 0, 0)
		if image:
			self.setImage(image)
		else:
			self.image = None

		
		
	def setImage(self, image):
		self.addImage(image, "original")
		self.chooseImage("original")

	def addImage(self, image, tag):
		self.images[tag] = image

	def chooseImage(self, tag):
		self.image = self.images[tag]
		self.currentTag = tag
		
		if not self.image:
			return

		center = self.rect.center
		self.rect.size = self.image.get_rect().size
		self.rect.center = center
		

	def draw(self, surface):
		if self.image:
			surface.blit(self.image, self.rect)