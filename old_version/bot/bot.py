from game.game import Game, Move
from bot.estimator import Estimator
from game.coordinate_system import Point

class Bot:
	def __init__(self, playerNumber, boardSize):
		self.game = Game(boardSize, "red")
		self.realBot = RealBot(self.game)

	def make_move(self):
		return self.realBot.makeMove().toTuple()

	def recieve_move(self, move):
		move = Move(*move)
		if self.game.moveIsValid(move):
			self.game.makeMove(move)
		else:
			print("invalid move recieved:", move)


class RealBot:
	def __init__(self, game):
		self.game = game

	def makeMove(self):
		estimator = Estimator(3, self.game.turn)
		move = estimator.bestMove(self.game)
		if self.game.moveIsValid(move):
			self.game.makeMove(move)
			return move
		else:
			print("illegal move recieved from estimator:", move)

	
