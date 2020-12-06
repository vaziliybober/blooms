from game_view.label import Label

class Counter(Label):
	def __init__(self, initialNumber):
		self.initialNumber = initialNumber
		self.number = initialNumber
		Label.__init__(self, str(initialNumber))

	def setNumber(self, number):
		self.number = number
		self.setText(str(number))

	def add(self, n):
		self.setNumber(self.number + n)

	def reset(self):
		self.setNumber(self.initialNumber)