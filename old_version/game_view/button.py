from game_view.label import Label
from game_view.images import images

class Button(Label):
	def __init__(self, text):
		Label.__init__(self, text)
		self.sprite.addImage(images.get("selected_label"), "selected")
		self.sprite.addImage(images.get("pressed_label"), "pressed")
		self.selected = False
		self.pressed = False

	def setSelected(self, flag):
		self.selected = flag
		if flag == True:
			self.sprite.chooseImage("selected")
		else:
			self.sprite.chooseImage("original")
			self.pressed = False

	def isSelected(self):
		return self.selected

	def setPressed(self, flag):
		self.pressed = flag
		if flag == True:
			self.sprite.chooseImage("pressed")
		else:
			self.sprite.chooseImage("original")
			self.selected = False

	def isPressed(self):
		return self.pressed