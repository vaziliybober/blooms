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
		self.addImage(image, "default")
		self.chooseImage("default")

	def addImage(self, image, tag):
		self.images[tag] = image

	def chooseImage(self, tag, align="center"):
		self.image = self.images[tag]
		self.currentTag = tag
		
		if not self.image:
			return

		if align == "center":
			center = self.rect.center
			self.rect.size = self.image.get_rect().size
			self.rect.center = center
		if align == "top":
			midtop = self.rect.midtop
			self.rect.size = self.image.get_rect().size
			self.rect.midtop = midtop
		if align == "bottom":
			midbottom = self.rect.midbottom
			self.rect.size = self.image.get_rect().size
			self.rect.midbottom = midbottom
		if align == "left":
			midleft = self.rect.midleft
			self.rect.size = self.image.get_rect().size
			self.rect.midleft = midleft
		if align == "right":
			midright = self.rect.midright
			self.rect.size = self.image.get_rect().size
			self.rect.midright = midright
		
	def draw(self, surface):
		if self.image:
			surface.blit(self.image, self.rect)