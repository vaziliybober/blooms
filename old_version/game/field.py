import game.functions as functions
from game.coordinate_system import Point, createHexagonMatrix
import general.timer as timer
import time

class Field:
	def __init__(self, coords):
		t = time.time()
		self.coords = coords
		self.stone = None
		self.bloom = None
		self.adjFields = None
		timer.fieldInit += (time.time() - t)

	def isEmpty(self):
		return bool(not self.stone)

	def clipStone(self, stone):
		self.stone = stone

	def isInBloom(self):
		return bool(self.bloom)

	def setBloom(self, bloom):
		self.bloom = bloom

	def setAdjFields(self, fields):
		self.adjFields = fields

	def __repr__(self):
		stone = 'E' if self.isEmpty() else functions.getColourAndTypeAsTwoLetters(self.stone.colour, self.stone.type)

		return '"F {}:{} {}"'.format(self.coords.x, self.coords.y, stone)


class FieldCollection:
	def __init__(self):
		self.fields = {}

	def add(self, field):
		t = time.time()
		self.fields[field.coords.toTuple()] = field
		timer.fieldAdd += (time.time() - t)
	def get(self, x=None, y=None):
		def getAllFields(fields):
			return fields.values()

		if x == None and y == None:
			return getAllFields(self.fields)

		return self.fields.get((x, y))

	def getAdjacentFields(self, field):
		if field.adjFields:
			return field.adjFields
		result = []
		for coords in createHexagonMatrix(Point(field.coords.x, field.coords.y), 1):
			adjField = self.get(coords.x, coords.y)
			if adjField:
				result.append(adjField)

		result.remove(field)

		field.setAdjFields(result)
		return result


	def copy(self):
		copyFields = FieldCollection()
		for key in self.fields:
			copyFields.add(Field(self.fields[key].coords))

		return copyFields



	def __repr__(self):
		return "Field Collection of {}".format(self.get())



















if __name__ == '__main__':
	field = Field(2, 4)
	from stone import Stone
	field.stone = Stone("red", "hollow")
	print(field)

	field2 = Field(-1, 3)
	fields = FieldCollection()
	fields.add(field)
	fields.add(field2)
	print()
	print(fields)
	print()
	print(fields.get())