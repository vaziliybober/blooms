
class Bloom:
	def __init__(self, fields):
		self.colour = fields[0].stone.colour
		self.type = fields[0].stone.type

		self.fields = []
		self.addFields(fields)

	def addField(self, field):
		self.fields.append(field)
		field.bloom = self

	def addFields(self, fields):
		for field in fields:
			self.addField(field)

	def get(self):
		return self.fields

	def __repr__(self):
		return "Bloom of {}".format(self.fields.__repr__())




class BloomCollection:
	def __init__(self):
		self.blooms = []

	def add(self, bloom):
		self.blooms.append(bloom)

	def get(self, colour=None, type=None):
		result = self.blooms

		if colour:
			result = [bloom for bloom in result if bloom.colour == colour]

		if type:
			result = [bloom for bloom in result if bloom.type == type]

		return result

	def remove(self, bloom):
		for field in bloom.get():
			field.bloom = None
		self.blooms.remove(bloom)

	def merge(self, bloom1, bloom2):
		bloom1.addFields(bloom2.get())
		self.blooms.remove(bloom2)

	def __repr__(self):
		return "BloomCollection of {}".format(self.blooms.__repr__())







if __name__ == '__main__':
	pass