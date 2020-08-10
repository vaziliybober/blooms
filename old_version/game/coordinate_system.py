
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def toTuple(self):
		return (self.x, self.y)

	def __repr__(self):
		return "({}:{})".format(self.x, self.y)


def createHexagonMatrix(centralPoint, size):
	result = []
	for x in range(centralPoint.x - size, centralPoint.x + size + 1):
		for y in range(centralPoint.y - size, centralPoint.y + size + 1):
			if abs((x - centralPoint.x) - (y - centralPoint.y)) <= size:
				result.append(Point(x, y))

	return result






if __name__ == '__main__':
	matrix = createHexagonMatrix(Point(0, 0), 2)
	print(matrix) 
	print(len(matrix))