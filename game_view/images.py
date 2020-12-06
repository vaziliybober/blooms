import pygame
import os


class Images:
	def __init__(self):
		self.images = {}

	def add(self, name, width=None, height=None):
		image = pygame.image.load(os.path.join("game_view", "resources", name + ".png"))
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

images.add("title_background")
images.add("field")
images.add("unavailable_field")
images.add("whole_unavailable_field")
images.add("hollow_unavailable_field")

images.add("red_whole_stone")
images.add("red_hollow_stone")
images.add("blue_whole_stone")
images.add("blue_hollow_stone")

images.add("label")
images.add("selected_label")
images.add("pressed_label")

images.add("red_score")
images.add("red_score_active")
images.add("red_hexagon")
images.add("red_hexagon_active")
images.add("blue_score")
images.add("blue_score_active")
images.add("blue_hexagon")
images.add("blue_hexagon_active")

images.add("blue_territory")
images.add("red_territory")

images.add("red_circle")
images.add("red_circle_active")
images.add("blue_circle")
images.add("blue_circle_active")

images.add("field_restriction")
images.add("whole_stone_restriction")
images.add("hollow_stone_restriction")


if __name__ == '__main__':
	rws = images.get("red_whole_stone")
	print(rws.get_rect().size)
	images.scale(5)
	rws = images.get("red_whole_stone")
	print(rws.get_rect().size)