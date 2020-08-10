from game.board import Board
import game.player as player


class Game:
	def __init__(self, boardSize):
		self.board = Board(boardSize)
		self.activePlayer = player.player1
		self.firstMove = True

	def firstMoveIsOn(self):
		return self.firstMove