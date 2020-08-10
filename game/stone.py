from general.utilities import Blanky, Opposite
from game.player import player1, player2

class StoneType(Blanky, Opposite):
	pass

type1 = StoneType("T1")
type2 = StoneType("T2")
type1.setOpposite(type2)
type2.setOpposite(type1)


class Stone:
	def __init__(self, type, player):
		self.type = type
		self.player = player

	def __repr__(self):
		result = "Stone({}, {})".format(self.type, self.player)
		return result

t1p1Stone = Stone(type1, player1)
t1p2Stone = Stone(type1, player2)
t2p1Stone = Stone(type2, player1)
t2p2Stone = Stone(type2, player2)

def get(type, player):
	if type == type1:
		if player == player1:
			return t1p1Stone
		if player == player2:
			return t1p2Stone
	if type == type2:
		if player == player1:
			return t2p1Stone
		if player == player2:
			return t2p2Stone


