import pygame


class Images:
	def __init__(self):
		self.images = {}

	def add(self, name, width=None, height=None):
		image = pygame.image.load("view/resources/" + name + ".png")
		if not width:
			width = image.get_rect().width
		if not height:
			height = image.get_rect().height

		if image.get_rect().size != (width, height):
			image = pygame.transform.scale(image, (width, height))

		self.images[name] = image

	def get(self, name):
		return self.images[name]

	def scale(self, multiplier):
		for name in self.images:
			image = self.images[name]
			rect = image.get_rect()
			self.images[name] = pygame.transform.scale(image, (int(rect.width * multiplier), int(rect.height * multiplier)))


images = Images()

images.add("stone11")
images.add("stone12")
images.add("stone21")
images.add("stone22")