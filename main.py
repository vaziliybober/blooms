import pygame
pygame.init()
import sys, os
import random
import time

import settings as s

import game_view.colours as colours
from game_view.images import images
from game_view.measurer import measurer
from game_view.game_view import GameView

from game.game import Game, Move, Player
from game.coordinate_system import Point

from bot.bot import Bot
from bot_jenya.bot import Bot as Bot_Jenya


def getComputerResolution():
	infoObject = pygame.display.Info()
	return (infoObject.current_w, infoObject.current_h)

def calculateScreenSize(x):
	(w, h) = getComputerResolution()
	os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (int(((1 - x) / 2) * w), int(((1 - x) / 2) * h))
	return (int(w * x), int(h * x))


def main():
	screen = pygame.display.set_mode(calculateScreenSize(s.screenSize))

	images.scale(s.scale)
	measurer.scale(s.scale)

	boardSize = s.boardSize

	firstPlayer = random.choice(["red"])

	if firstPlayer == "red":
		redPlayerTurn = 1
		bluePlayerTurn = 2
	if firstPlayer == "blue":
		redPlayerTurn = 2
		bluePlayerTurn = 1

	bot1 = Bot(redPlayerTurn, boardSize)
	bot2 = Bot_Jenya(bluePlayerTurn, boardSize)

	redPlayer = Player("red")
	redPlayer.setName("Player 1")
	bluePlayer = Player("blue")
	bluePlayer.setName("Player 2")
	players = {}
	players[redPlayer.colour] = redPlayer
	players[bluePlayer.colour] = bluePlayer

	game = Game(boardSize, firstPlayer)
	gameView = GameView(game, screen, players)

	firstStone = None
	firstCoords = None

	botJustMadeAMove = False

	while True:
		if game.isOver():
			print("Game is over! {} wins. Number of turns: {}".format(players[game.getWinner()].name, len(game.history)))
			break

		currentPlayer = players[game.turn]

		if currentPlayer.isBot():
			start_time = time.time()
			move = Move(*currentPlayer.bot.make_move())
			timeDelta = time.time() - start_time
			timeToWait = 0 - timeDelta
			if timeToWait > 0:
				time.sleep(timeToWait)
			if not game.moveIsValid(move):
				move = Move((), ())

			game.makeMove(move)
			currentPlayer = players[game.turn]
			if currentPlayer.isBot():
				currentPlayer.bot.recieve_move(move.toTuple())
			gameView.update()


			botJustMadeAMove = True

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if botJustMadeAMove:
				botJustMadeAMove = False
				break

			if event.type == pygame.MOUSEMOTION:
				if gameView.passButton.sprite.rect.collidepoint(event.pos):
					if not gameView.passButton.isPressed():
						gameView.passButton.setSelected(True)
				else:
					gameView.passButton.setSelected(False)

			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if gameView.passButton.sprite.rect.collidepoint(event.pos):
					gameView.passButton.setSelected(True)
					if game.passIsValid():
						game.pass_()
						currentPlayer = players[game.turn]
						if currentPlayer.isBot():
							if firstStone:
								if firstStone == "whole":
									move = (firstCoords.toTuple(), None)
								else:
									move = (None, firstCoords.toTuple())
								currentPlayer.bot.recieve_move(move)
							else:
								currentPlayer.bot.recieve_move(((), ()))
						gameView.update()
						firstStone = None


			if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3):
				if event.button == 1 and gameView.passButton.sprite.rect.collidepoint(event.pos):
					gameView.passButton.setPressed(True)

				if event.button == 1:
					type = "whole"
				else:
					type = "hollow"

				field = gameView.getFieldByCoords(event.pos)
				if not field:
					continue

				coords = Point(field.coords.x, field.coords.y)

				if firstStone == None:
					if game.firstStoneIsValid(coords, type):
						game.placeFirstStone(coords, type)
						firstStone = type
						firstCoords = coords
						gameView.update()
				elif not type == firstStone:
					if game.secondStoneIsValid(coords, type):
						game.placeSecondStone(coords, type)

						currentPlayer = players[game.turn]
						if currentPlayer.isBot():
							if firstStone == "whole":
								move = (firstCoords.toTuple(), coords.toTuple())
							else:
								move = (coords.toTuple(), firstCoords.toTuple())
							currentPlayer.bot.recieve_move(move)
						gameView.update()
						firstStone = None



		gameView.draw()

		pygame.display.flip()





if __name__ == '__main__':
	main()
