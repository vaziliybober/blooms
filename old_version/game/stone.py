import game.functions as functions





class FakeStone:
	def __init__(self, colour, type):
		self.colour = colour
		self.type = type

	def equals(self, another):
		return (self is another)

	def __repr__(self):
		return '"S {}"'.format(functions.getColourAndTypeAsTwoLetters(self.colour, self.type))

redWholeStone = FakeStone("red", "whole")
redHollowStone = FakeStone("red", "hollow")
blueWholeStone = FakeStone("blue", "whole")
blueHollowStone = FakeStone("blue", "hollow")

def Stone(colour, type):
	if colour == "red":
		if type == "whole":
			return redWholeStone
		if type == "hollow":
			return redHollowStone
	if colour == "blue":
		if type == "whole":
			return blueWholeStone
		if type == "hollow":
			return blueHollowStone







if __name__ == '__main__':
	stone = Stone("blue", "whole")
	print(stone)
