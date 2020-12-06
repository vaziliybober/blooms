
def getColourAndTypeAsTwoLetters(colour, type):
	return "{}{}".format(colour[0].upper(), type[0].upper())

def opposite(thing):
	if thing == "red":
		return "blue"
	if thing == "blue":
		return "red"
	if thing == "whole":
		return "hollow"
	if thing == "hollow":
		return "whole"











if __name__ == '__main__':
	print(getColourAndTypeAsTwoLetters("red", "hollow"))