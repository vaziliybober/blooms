from game.field import Field, FieldCollection
from game.bloom import Bloom, BloomCollection
from game.stone import Stone
from game.coordinate_system import Point, createHexagonMatrix
import general.timer as timer
import time


class Board:
	def __init__(self, size, copy=False):
		def createFields():
			fields = FieldCollection()
			t = time.time()
			matrix = createHexagonMatrix(Point(0, 0), size)
			timer.board_init += (time.time() - t)
			for coords in matrix:
				fields.add(Field(coords))

			return fields

		self.size = size
		if not copy:
			self.fields = createFields()
		self.blooms = BloomCollection()

	def placeStone(self, stone, coords):
		def addStoneToBlooms(stone, field):
			adjFields = self.fields.getAdjacentFields(field)
			for adjField in adjFields:
				if adjField.isEmpty():
					continue

				if (adjField.bloom.colour, adjField.bloom.type) == (stone.colour, stone.type):
					if not field.isInBloom():
						adjField.bloom.addField(field)
					else:
						if not field.bloom is adjField.bloom:
							self.blooms.merge(adjField.bloom, field.bloom)

			if not field.isInBloom():
				self.blooms.add(Bloom([field]))

		field = self.fields.get(coords.x, coords.y)
		if not field:
			return
		field.clipStone(stone)
		t = time.time()
		addStoneToBlooms(stone, field)
		timer.addStoneToBlooms += (time.time() - t)
	
	def bloomIsFenced(self, bloom):
		for field in bloom.get():
			for adjField in self.fields.getAdjacentFields(field):
				if adjField.isEmpty():
					return False

		return True

	def removeBloom(self, bloom):
		for field in bloom.get():
			field.stone = None
		self.blooms.remove(bloom)

	def getTerritory(self, colour):
		def expand(field, emptyGroup, checkedFields):
			checkedFields.append(field)
			emptyGroup.append(field)

			for adjField in self.fields.getAdjacentFields(field):
				if adjField in checkedFields:
					continue

				if adjField.isEmpty() and not adjField in checkedFields:
					expand(adjField, emptyGroup, checkedFields)
						
					


		territory = []
		checkedFields = []
		touchesColour = False

		for field in self.fields.get():
			emptyGroup = []

			if field in checkedFields or not field.isEmpty():
				continue

			expand(field, emptyGroup, checkedFields)

			for emptyField in emptyGroup:
				for adjField in self.fields.getAdjacentFields(emptyField):
					if not adjField.isEmpty():
						if adjField.stone.colour != colour:
							emptyGroup = []
							break
						else:
							touchesColour = True

			if not touchesColour:
				emptyGroup = []

			territory += emptyGroup

		return territory




	def getScore(self, colour):
		return self.getNumberOfStones(colour) + self.getTerritoryScore(colour)

	def getTerritoryScore(self, colour):
		return len(self.getTerritory(colour))

	def getNumberOfStones(self, colour):
		counter = 0
		for field in self.fields.get():
			if not field.isEmpty() and field.stone.colour == colour:
				counter += 1

		return counter

	def copy(self, noBlooms=False):
		t = time.time()
		copyBoard = Board(self.size, True)
		copyBoard.fields = self.fields.copy()
		timer.board += (time.time() - t)

		for bloom in self.blooms.get():
			copyFields = []
			for field in bloom.get():
				copyStone = Stone(field.stone.colour, field.stone.type)
				copyField = copyBoard.fields.get(field.coords.x, field.coords.y)
				copyField.stone = copyStone
				if not noBlooms:
					copyFields.append(copyField)

			if not noBlooms:
				copyBoard.blooms.add(Bloom(copyFields))

		return copyBoard

	def equals(self, another):
		for field in self.fields.get():
			anotherField = another.fields.get(field.coords.x, field.coords.y)
			if field.isEmpty() != anotherField.isEmpty():
				return False
			if not field.isEmpty() and not field.stone.equals(anotherField.stone):
				return False

		return True





if __name__ == '__main__':
	board = Board(2)

	#print(board.fields.get())
	#print(len(board.fields.get()))

	#print(board.fields.getAdjacentFields(board.fields.get(-1, -2)))

	#print(board.blooms)

	from stone import Stone

	board.placeStone(Stone("blue", "whole"), Point(0, 0))
	board.placeStone(Stone("blue", "whole"), Point(1, 1))

	board.placeStone(Stone("blue", "whole"), Point(-2, -1))

	board.placeStone(Stone("blue", "whole"), Point(-1, -2))
	board.placeStone(Stone("blue", "whole"), Point(0, -2))
	board.placeStone(Stone("blue", "whole"), Point(1, -1))

	#print(board.blooms)

	board.placeStone(Stone("blue", "whole"), Point(-1, -1))

	board.placeStone(Stone("blue", "whole"), Point(0, 2))
	board.placeStone(Stone("blue", "hollow"), Point(-1, 1))
	board.placeStone(Stone("blue", "hollow"), Point(0, 1))
	board.placeStone(Stone("blue", "hollow"), Point(1, 2))
	print(board.bloomIsFenced(board.fields.get(0, 2).bloom))

	print(board.blooms)
	