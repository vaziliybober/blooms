
class Measurer:
	def __init__(self):
		self.distances = {}

	def add(self, name, value):
		self.distances[name] = value

	def get(self, name):
		return self.distances[name]

	def scale(self, multiplier):
		for name in self.distances:
			self.distances[name] = int(self.distances[name] * multiplier)

measurer = Measurer()

measurer.add("default text size", 30)
measurer.add("title text size", 40)
measurer.add("from pass to board", 20)
measurer.add("from score to board", 100)
measurer.add("from score to counters", 60)
measurer.add("from one territory counter to stone counter", 200)
measurer.add("from score to player name", 30)
measurer.add("from title to board", 30)