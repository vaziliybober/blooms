from game.board import Board
from game.stone import Stone
from game.coordinate_system import Point
from game.functions import opposite
import general.timer as timer
import time

class Move:
	def __init__(self, wholeCoords, hollowCoords):
		if type(wholeCoords) in (tuple, list):
			self.wholeCoords = Point(*wholeCoords) if wholeCoords else None
		else:
			self.wholeCoords = wholeCoords

		if type(hollowCoords) in (tuple, list):
			self.hollowCoords = Point(*hollowCoords) if hollowCoords else None
		else:
			self.hollowCoords = hollowCoords

	def toTuple(self):
		wholeCoords = self.wholeCoords.toTuple() if self.wholeCoords else ()
		hollowCoords = self.hollowCoords.toTuple() if self.hollowCoords else ()

		return (wholeCoords, hollowCoords)

	def isEmpty(self):
		return bool(not self.wholeCoords and not self.hollowCoords)

	def __repr__(self):
		return self.toTuple().__repr__()


class Player:
	def __init__(self, colour, bot=None):
		self.colour = colour
		self.bot = None if bot in (None, "human") else bot
		self.name = ""

	def isBot(self):
		return bool(self.bot)

	def isHuman(self):
		return bool(not self.isBot())

	def setName(self, name):
		self.name = name


class Game:
	def __init__(self, boardSize, firstPlayer, copy=False):
		if copy:
			return

		self.board = Board(boardSize)
		self.firstMove = True
		self.turn = firstPlayer
		self.gameIsAboutToBeOver = False
		self.gameIsOver = False
		self.moveIsNotFinished = False
		self.history = []

	def copy(self, noBlooms=False):
		t = time.time()
		copyGame = Game(self.board.size, self.turn, True)
		t2 = time.time()
		copyGame.board = self.board.copy(noBlooms)
		timer.boardCopy += (time.time() - t2)
		copyGame.firstMove = self.firstMove
		copyGame.turn = self.turn
		copyGame.gameIsAboutToBeOver = self.gameIsAboutToBeOver
		copyGame.gameIsOver = self.gameIsOver
		copyGame.moveIsNotFinished = self.moveIsNotFinished
		copyGame.history = []
		for game in self.history:
			copyGame.history.append(game)

		timer.copy += (time.time() - t)

		return copyGame

	def equals(self, another):
		t = time.time()
		result = bool(self.board.equals(another.board) and self.turn == another.turn)
		timer.equals += (time.time() - t)
		return result

	def nextTurn(self):
		t = time.time()
		self.firstMove = False
		self.turn = opposite(self.turn)

		bloomsToRemove = []
		for bloom in self.board.blooms.get(self.turn):
			if self.board.bloomIsFenced(bloom):
				bloomsToRemove.append(bloom)

		for bloomToRemove in bloomsToRemove:
			self.board.removeBloom(bloomToRemove)

		self.history.append(self.copy(True))

		timer.nextTurn += (time.time() - t)

	def moveIsValid(self, move):
		t = time.time()
		if (move.wholeCoords and move.hollowCoords or not move.wholeCoords and not move.hollowCoords) and self.firstMove:
			timer.moveIsValid += (time.time() - t)
			return False

		wholeField = None
		hollowField = None

		if move.wholeCoords:
			wholeField = self.board.fields.get(move.wholeCoords.x, move.wholeCoords.y)
			if not wholeField or not wholeField.isEmpty():
				timer.moveIsValid += (time.time() - t)
				return False

		if move.hollowCoords:
			hollowField = self.board.fields.get(move.hollowCoords.x, move.hollowCoords.y)
			if not hollowField or not hollowField.isEmpty():
				timer.moveIsValid += (time.time() - t)
				return False
		
		if wholeField is hollowField and wholeField != None:
			timer.moveIsValid += (time.time() - t)
			return False

		if not move.wholeCoords and not move.hollowCoords:
			timer.moveIsValid += (time.time() - t)
			return True
			
		copyGame = self.copy()
		copyGame.makeMove(move)

		for game in self.history:
			if game.equals(copyGame):
				timer.moveIsValid += (time.time() - t)
				return False

		for bloom in copyGame.board.blooms.get(opposite(copyGame.turn)):
			if copyGame.board.bloomIsFenced(bloom):
				timer.moveIsValid += (time.time() - t)
				return False

		timer.moveIsValid += (time.time() - t)
		return True

	def makeMove(self, move):
		t = time.time()
		if move.isEmpty():
			self.pass_()
			return

		self.gameIsAboutToBeOver = False

		wholeStone = Stone(self.turn, "whole")
		hollowStone = Stone(self.turn, "hollow")

		if move.wholeCoords:
			self.board.placeStone(wholeStone, move.wholeCoords)
		if move.hollowCoords:
			self.board.placeStone(hollowStone, move.hollowCoords)

		self.nextTurn()
		timer.makeMove += (time.time() - t)

	def isOver(self):
		return self.gameIsOver

	def getWinner(self):
		if not self.isOver:
			return None

		redScore = self.board.getScore("red")
		blueScore = self.board.getScore("blue")

		if redScore > blueScore:
			return "red"
		if blueScore > redScore:
			return "blue"
		else:
			return self.turn
	
	def firstStoneIsValid(self, coords, type):
		if not self.board.fields.get(coords.x, coords.y).isEmpty():
			return False

		copyGame = self.copy()
		copyGame.placeFirstStone(coords, type)

		if copyGame.passIsValid():
			return True

		for field in copyGame.board.fields.get():
			if not field.isEmpty():
				continue

			if copyGame.secondStoneIsValid(field.coords, opposite(type)):
				return True

		return False

	def placeFirstStone(self, coords, type):
		self.moveIsNotFinished = True
		self.gameIsAboutToBeOver = False
		stone = Stone(self.turn, type)
		self.board.placeStone(stone, coords)

	def secondStoneIsValid(self, coords, type):
		if self.firstMove:
			return False

		if not self.board.fields.get(coords.x, coords.y).isEmpty():
			return False

		copyGame = self.copy()
		copyGame.placeSecondStone(coords, type)

		for game in self.history:
			if game.equals(copyGame):
				return False

		for bloom in copyGame.board.blooms.get(opposite(copyGame.turn)):
			if copyGame.board.bloomIsFenced(bloom):
				return False

		return True

	def placeSecondStone(self, coords, type):
		self.moveIsNotFinished = False
		stone = Stone(self.turn, type)

		self.board.placeStone(stone, coords)
		self.nextTurn()

	def passIsValid(self):
		if not self.moveIsNotFinished:
			if self.firstMove:
				return False
		else:
			copyGame = self.copy()
			copyGame.pass_()

			for game in self.history:
				if game.equals(copyGame):
					return False

			for bloom in copyGame.board.blooms.get(opposite(copyGame.turn)):
				if copyGame.board.bloomIsFenced(bloom):
					return False


		return True

	def pass_(self):
		if not self.moveIsNotFinished:
			if self.gameIsAboutToBeOver:
				self.gameIsOver = True
			else:
				self.gameIsAboutToBeOver = True

		self.moveIsNotFinished = False

		self.nextTurn()

