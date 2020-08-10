from game_view.board_view import BoardView
from game_view.button import Button
from game_view.counter import Counter
from game_view.label import Label
from game_view.measurer import measurer
from game_view.images import images
import game_view.colours as colours

class GameView:
	def __init__(self, game, screen, players):
		self.game = game
		self.screen = screen
		self.players = players
		self.boardView = BoardView(game.board, game)
		self.boardView.sprite.rect.center = screen.get_rect().center

		self.title = Label("BLOOMS")
		self.title.sprite.setImage(images.get("title_background"))
		self.title.setTextColour(colours.WHITE)
		self.title.setTextSize(measurer.get("title text size"))
		self.title.sprite.rect.midbottom = self.boardView.sprite.rect.midtop
		self.title.sprite.rect.y -= measurer.get("from title to board")

		self.passButton = Button("PASS")
		self.passButton.setTextColour(colours.ORANGE)
		self.passButton.sprite.rect.midtop = self.boardView.sprite.rect.midbottom
		self.passButton.sprite.rect.y += measurer.get("from pass to board")

		self.redScore = Counter(self.game.board.getScore("red"))
		self.redScore.sprite.setImage(images.get("red_score"))
		self.redScore.sprite.addImage(images.get("red_score_active"), "active")
		self.redScore.sprite.rect.midright = self.boardView.sprite.rect.midleft
		self.redScore.sprite.rect.x -= measurer.get("from score to board")

		self.redTerritoryScore = Counter(self.game.board.getTerritoryScore("red"))
		self.redTerritoryScore.sprite.setImage(images.get("red_hexagon"))
		self.redTerritoryScore.sprite.rect.midtop = self.redScore.sprite.rect.midbottom
		self.redTerritoryScore.sprite.rect.y += measurer.get("from score to counters")
		self.redTerritoryScore.sprite.rect.x += measurer.get("from one territory counter to stone counter") / 2

		self.redStoneCounter = Counter(self.game.board.getNumberOfStones("red"))
		self.redStoneCounter.sprite.setImage(images.get("red_circle"))
		self.redStoneCounter.sprite.rect.midtop = self.redScore.sprite.rect.midbottom
		self.redStoneCounter.sprite.rect.y += measurer.get("from score to counters")
		self.redStoneCounter.sprite.rect.x -= measurer.get("from one territory counter to stone counter") / 2.2

		self.redPlayerName = Label(players["red"].name)
		self.redPlayerName.sprite.setImage(None)
		self.redPlayerName.sprite.rect.midbottom = self.redScore.sprite.rect.midtop
		self.redPlayerName.sprite.rect.y -= measurer.get("from score to player name")

		if self.game.turn == "red":
			self.redScore.sprite.chooseImage("active")
			self.redTerritoryScore.sprite.setImage(images.get("red_hexagon_active"))
			self.redStoneCounter.sprite.setImage(images.get("red_circle_active"))
			self.redPlayerName.setTextColour(colours.ORANGE)
			self.redScore.setTextColour(colours.ORANGE)
			self.redStoneCounter.setTextColour(colours.ORANGE)
			self.redTerritoryScore.setTextColour(colours.ORANGE)




		self.blueScore = Counter(self.game.board.getScore("blue"))
		self.blueScore.sprite.setImage(images.get("blue_score"))
		self.blueScore.sprite.addImage(images.get("blue_score_active"), "active")
		self.blueScore.sprite.rect.midleft = self.boardView.sprite.rect.midright
		self.blueScore.sprite.rect.x += measurer.get("from score to board")

		self.blueTerritoryScore = Counter(self.game.board.getTerritoryScore("blue"))
		self.blueTerritoryScore.sprite.setImage(images.get("blue_hexagon"))
		self.blueTerritoryScore.sprite.rect.midtop = self.blueScore.sprite.rect.midbottom
		self.blueTerritoryScore.sprite.rect.y += measurer.get("from score to counters")
		self.blueTerritoryScore.sprite.rect.x += measurer.get("from one territory counter to stone counter") / 2

		self.blueStoneCounter = Counter(self.game.board.getNumberOfStones("blue"))
		self.blueStoneCounter.sprite.setImage(images.get("blue_circle"))
		self.blueStoneCounter.sprite.rect.midtop = self.blueScore.sprite.rect.midbottom
		self.blueStoneCounter.sprite.rect.y += measurer.get("from score to counters")
		self.blueStoneCounter.sprite.rect.x -= measurer.get("from one territory counter to stone counter") / 2.2

		self.bluePlayerName = Label(players["blue"].name)
		self.bluePlayerName.sprite.setImage(None)
		self.bluePlayerName.sprite.rect.midbottom = self.blueScore.sprite.rect.midtop
		self.bluePlayerName.sprite.rect.y -= measurer.get("from score to player name")

		if self.game.turn == "blue":
			self.blueScore.sprite.chooseImage("active")
			self.blueTerritoryScore.sprite.setImage(images.get("blue_hexagon_active"))
			self.blueStoneCounter.sprite.setImage(images.get("blue_circle_active"))
			self.bluePlayerName.setTextColour(colours.ORANGE)
			self.blueScore.setTextColour(colours.ORANGE)
			self.blueStoneCounter.setTextColour(colours.ORANGE)
			self.blueTerritoryScore.setTextColour(colours.ORANGE)

		self.screen.fill(colours.WHITE)

	def getFieldByCoords(self, coords):
		relativeCoords = [None, None]
		relativeCoords[0] = coords[0] - self.boardView.sprite.rect.x 
		relativeCoords[1] = coords[1] - self.boardView.sprite.rect.y
		return self.boardView.getFieldByCoords(relativeCoords)

	def update(self):
		self.__init__(self.game, self.screen, self.players)

	def draw(self):
		self.boardView.draw(self.screen)

		self.title.draw(self.screen)

		self.passButton.draw(self.screen)

		self.redScore.draw(self.screen)

		self.redTerritoryScore.draw(self.screen)

		self.redStoneCounter.draw(self.screen)

		self.redPlayerName.draw(self.screen)

		self.blueScore.draw(self.screen)

		self.blueTerritoryScore.draw(self.screen)

		self.blueStoneCounter.draw(self.screen)

		self.bluePlayerName.draw(self.screen)