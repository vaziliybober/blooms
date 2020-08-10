
class Opposite:
	def setOpposite(self, opposite):
		self.opposite = opposite


class Blanky:
	def __init__(self, repr=None):
		if repr == None:
			repr = super().__repr__()

		self.repr = repr

	def __repr__(self):
		return self.repr