from game.functions import opposite
from game.game import Move
import general.timer as timer
import time

class Estimator:
	def __init__(self, depth, colour):
		self.colour = colour
		self.depth = depth

		self.stoneReward = 10
		self.territoryReward = 2
		self.safetyReward = 1

		self.numberOfOperations = 0


	def countStoneReward(self, game, colour):
		return self.stoneReward * (game.board.getNumberOfStones(colour) - game.board.getNumberOfStones(opposite(colour)))

	def countTerritoryReward(self, game, colour):
		return self.territoryReward * (game.board.getTerritoryScore(colour) - game.board.getTerritoryScore(opposite(colour)))

	def countSafetyReward(self, game, colour):
		def countAdjEmptyFields():
			for bloom in game.board.blooms.get():
				for field in bloom.get():
					for adjField in game.board.fields.getAdjacentFields(field):
						if adjField.isEmpty() and not adjField in adjEmptyFields:
							adjEmptyFields.append(adjField)

		adjEmptyFields = []
		countAdjEmptyFields()

		return len(adjEmptyFields) * self.safetyReward


	def estimate(self, game, colour):
		return self.countStoneReward(game, colour) + self.countSafetyReward(game, colour)

	def getMoves(self, game):
		t = time.time()
		if game.firstMove:
			return [Move((0, 0), None)]

		if game.gameIsAboutToBeOver:
			if game.board.getScore(game.turn) > game.board.getScore(opposite(game.turn)):
				return [Move(None, None)]

		lonelyFields = []
		wholeFields = []
		hollowFields = []
		preChosenMoves = []
		for field in game.board.fields.get():
			if not field.isEmpty():
				continue
		
			for adjField in game.board.fields.getAdjacentFields(field):
				if not adjField.isEmpty():
					if adjField.stone.type == "whole":
						wholeFields.append(field)
					else:
						hollowFields.append(field)
					break

			else:
				lonelyFields.append(field)


		if not hollowFields and lonelyFields:
			hollowFields.append(lonelyFields[0])

		if not wholeFields and lonelyFields:
			wholeFields.append(lonelyFields[0])


		for wholeField in wholeFields:
			for hollowField in hollowFields:
				move = Move(wholeField.coords, hollowField.coords)
				if game.moveIsValid(move):
					preChosenMoves.append(move)


		if not hollowFields and not lonelyFields:
			for wholeField in wholeFields:
				move = Move(wholeField.coords, None)
				if game.moveIsValid(move):
					preChosenMoves.append(move)

		if not wholeFields and not lonelyFields:
			for hollowField in hollowFields:
				move = Move(None, hollowField.coords)
				if game.moveIsValid(move):
					preChosenMoves.append(move)

		timer.pre += (time.time() - t)

		t = time.time()
		movesDict = {}
		for move in preChosenMoves:
			copyGame = game.copy()
			copyGame.makeMove(move)
			estimation = self.estimate(copyGame, game.turn)
			if not movesDict.get(estimation):
				movesDict[estimation] = []
			movesDict[estimation].append(move)


		moves = []
		if game.board.getScore(game.turn) >= game.board.getScore(opposite(game.turn)):
			moves.append(Move(None, None))

		n = 0
		N = 10
		for key in sorted(movesDict.keys()):
			for move in movesDict[key]:
				moves.append(move)
				n += 1

				if n == N:
					timer.post += (time.time() - t)
					return moves

		if not moves:
			timer.post += (time.time() - t)
			return [Move(None, None)]

		timer.post += (time.time() - t)
		return moves

		




	def minimax(self, game, alpha, beta, currentDepth, isMax):
		if game.firstMove:
			return Move((0, 0), None)
		if currentDepth == self.depth:
			self.numberOfOperations += 1
			t = time.time()
			esteem = self.estimate(game, opposite(game.turn))
			timer.estimationTime += (time.time() - t)
			return esteem
		t = time.time()
		#possibleMoves = self.getMoves(game)
		timer.possibleMoves += (time.time() - t)
		v = None
		vMove = None
		theMove = None
		t = time.time()
		fields = game.board.fields.get()
		timer.fieldsGet += (time.time() - t)
		N = 33
		n = 0
		for wholeField in fields:

			for adjField in game.board.fields.getAdjacentFields(wholeField):
				if not adjField.isEmpty() and (adjField.stone.type == "whole"):
					break
			else:
				continue

			for hollowField in fields:
				if n == N:
					n = 0
					if currentDepth == 0:
						return theMove
					return v

				for adjField in game.board.fields.getAdjacentFields(hollowField):
					if not adjField.isEmpty() and (adjField.stone.colour != self.colour or adjField.stone.type == "hollow"):
						break
				else:
					continue

				move = Move(wholeField.coords, hollowField.coords)
				if not game.moveIsValid(move):
					continue

				n += 1

				theMove = move
				nextGameState = game.copy()
				nextGameState.makeMove(move)

				newV = self.minimax(nextGameState, alpha, beta, currentDepth + 1, bool(not isMax))

				if isMax:
					if v == None or newV > v:
						v = newV

					if beta != None and newV >= beta:
						if currentDepth == 0:
							return theMove
						return v

					if alpha == None or newV > alpha:
						alpha = newV

				else:
					if v == None or newV < v:
						v = newV

					if alpha != None and newV <= alpha:
						if currentDepth == 0:
							return theMove
						return v

					if beta == None or newV < beta:
						beta = newV

		if currentDepth == 0:
			if not theMove:
				return Move(None, None)
			return theMove

		if not v:
			nextGameState = game.copy()
			nextGameState.makeMove(Move(None, None))
			return self.minimax(nextGameState, alpha, beta, currentDepth + 1, bool(not isMax))
		return v

	def bestMove(self, game):
		t = time.time()
		b = self.minimax(game, None, None, 0, True)
		print("Number of operations: {}\nTime: {}\nCopy time: {}\nEquals time: {}\nBoard init time: {}\nMove is valid time: {}\nPossible moves time: {}\nPre: {}\nPost: {}\nAdd stone to blooms time: {}\nNext turn time: {}\nFields get time: {}\nMake move time: {}\nEstimation time: {}\nBoard copy time: {}\nBoard time: {}\nField init time: {}\nField add: {}\n".format(self.numberOfOperations, time.time() - t, timer.copy, timer.equals, timer.board_init, timer.moveIsValid, timer.possibleMoves, timer.pre, timer.post, timer.addStoneToBlooms, timer.nextTurn, timer.fieldsGet, timer.makeMove, timer.estimationTime, timer.boardCopy, timer.board, timer.fieldInit, timer.fieldAdd))
		timer.copy = 0
		timer.equals = 0
		self.numberOfOperations = 0
		if not b:
			print("not b")
		return b

