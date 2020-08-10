from general.utilities import Blanky, Opposite

class Player(Blanky, Opposite):
	pass

player1 = Player("P1")
player2 = Player("P2")
player1.setOpposite(player2)
player2.setOpposite(player1)