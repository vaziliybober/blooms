

def isInMatrix(point, centralPoint, matrixSize):
	return bool(abs((point[0] - centralPoint[0]) - (point[1] - centralPoint[1])) <= matrixSize)

def createHexagonMatrix(centralPoint, size):
	result = []
	for x in range(centralPoint[0] - size, centralPoint[0] + size + 1):
		for y in range(centralPoint[1] - size, centralPoint[1] + size + 1):
			if isInMatrix((x, y), centralPoint, size):
				result.append((x, y))

	return result


class Board:
	def __init__(self, size, copy=False):
		self.size = size

		if copy:
			return

		self.stones = {}
		self.matrix = createHexagonMatrix((0, 0), self.size)

	def isInMatrix(self, coords):
		return isInMatrix(coords, (0, 0), self.size)

	def placeStone(self, stone, coords):
		self.stones[coords] = stone


