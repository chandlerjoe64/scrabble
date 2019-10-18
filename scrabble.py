import pygame
import string
import time
import random
from copy import deepcopy

#TODOS
#implement blank tiles
#handle empty letter bag on player tile draws
#add text for multiplier squares
#swap tiles
#pass play
#implement second player
#implement game-over when out of tiles or out of plays
#descriptive messages on invalid plays
#change tile modifiers after a successful play
#implement logging feature for plays/failures


#function definitions
def getCoordinate(mousePosition):
	#convert mouse coordinates into gameboard coordinates
	x,y = int((float(mousePosition[0]) / float(gameSize * blockSize)) * float(gameSize)),int((float(mousePosition[1]) / float(gameSize * blockSize)) * float(gameSize)) 
	return (x,y)

def placeTile(coordinates, playerTileIndex):
	#check if cursor is in valid location for placement
	if coordinates[1] > (gameSize - 1):
		return
	#check if tile is already populated
	if tiles[coordinates[0]][coordinates[1]][3] != None:
		return
	#check if player tile is valid (end-game scenarios)
	if playerTiles[playerTileIndex][1]:
		return
	character = playerTiles[playerTileIndex][0]
	#update player tile
	playerTiles[playerTileIndex][1] = True
	#update tile
	tiles[coordinates[0]][coordinates[1]][3] = character
	#repaint tile
	pygame.draw.rect(screen, brown, pygame.Rect(((coordinates[0]*blockSize)+1),(coordinates[1]*blockSize),(blockSize-2),(blockSize-2)))
	#place letter
	xOffset = (blockSize - font.size(character)[0]) / 2
	yOffset = (blockSize - font.size(character)[1]) / 2
	screen.blit(font.render(character, True, (0,0,0)), (((coordinates[0] * blockSize) + xOffset), ((coordinates[1] * blockSize)) + yOffset))
	#gray out placed player tiles
	pygame.draw.rect(screen, gray, pygame.Rect(((blockSize * (4+playerTileIndex)),((gameSize*blockSize) + int(blockSize * .5)),(blockSize-2),(blockSize-2))))

def selectTile(coordinates):
	#check if cursor is in valid location for selection #TODO improve bounds indentification here
	if coordinates[0] > 3 and coordinates[0] < 11 and coordinates[1] > gameSize-1:
		return coordinates[0] - 4
	else:
		return ''

def setupTiles(tiles):
	for x in range(gameSize):
		for y in range(gameSize):
			if x==7 and y==7:
				modifier = (1,2)
			#double word
			elif (x,y) in doubleWords:
				modifier = (1,2)
			#double letter
			elif (x,y) in doubleLetters:
				modifier = (2,1)
			#triple word
			elif (x,y) in tripleWords:
				modifier = (1,3)
			#triple letter
			elif (x,y) in tripleLetters:
				modifier = (3,1)
			#plain square
			else:
				modifier = (1,1)
			#x coord, y coord, modifier, letter,locked
			tiles[x][y] = [x,y,modifier,None, False]

def setupBoard():
	for x in range(gameSize):
		for y in range(gameSize):
			#center
			if x==7 and y==7:
				tileColor = pink
			#double word
			elif (x,y) in doubleWords:
				tileColor = pink
			#double letter
			elif (x,y) in doubleLetters:
				tileColor = lightBlue
			#triple word
			elif (x,y) in tripleWords:
				tileColor = red
			#triple letter
			elif (x,y) in tripleLetters:
				tileColor = darkBue
			#plain square
			else:
				tileColor = beige

			pygame.draw.rect(screen, tileColor, pygame.Rect(((x*blockSize)+1),(y*blockSize),(blockSize-2),(blockSize-2)))

def updateScore(turnScore,gameScore):
	#clear previous blits
	pygame.draw.rect(screen, white, pygame.Rect(((blockSize * 11),(gameSize*blockSize),(blockSize * 4),(blockSize * 2))))

	#Turn
	xOffset = (blockSize - font.size(str(turnScore))[0]) / 2
	yOffset = (blockSize - font.size(str(turnScore))[1]) / 2

	screen.blit(font.render(str(turnScore), True, (0,0,0)),((blockSize * 12) + xOffset, (gameSize*blockSize) + yOffset))

	xOffsetSub = (blockSize - subFont.size("Turn")[0]) / 2
	yOffsetSub = (blockSize - subFont.size("Turn")[1]) / 2
	screen.blit(subFont.render("Turn", True, red),((blockSize * 14) + xOffsetSub, (gameSize*blockSize) + yOffsetSub))

	#Game
	xOffset = (blockSize - font.size(str(gameScore))[0]) / 2
	yOffset = (blockSize - font.size(str(gameScore))[1]) / 2

	screen.blit(font.render(str(gameScore), True, (0,0,0)),((blockSize * 12) + xOffset, ((gameSize + 1)*blockSize) + yOffset))

	xOffsetSub = (blockSize - subFont.size("Game")[0]) / 2
	yOffsetSub = (blockSize - subFont.size("Game")[1]) / 2
	screen.blit(subFont.render("Game", True, red),((blockSize * 14) + xOffsetSub, ((gameSize + 1)*blockSize) + yOffsetSub))

def setupPlayerTiles():
	color = brown
	for x in range(7):
		character = letterBag.pop()
		xOffset = (blockSize - font.size(character)[0]) / 2
		yOffset = (blockSize - font.size(character)[1]) / 2

		pygame.draw.rect(screen, color, pygame.Rect(((blockSize * (4+x)),((gameSize*blockSize) + int(blockSize * .5)),(blockSize-2),(blockSize-2))))
		screen.blit(font.render(character, True, (0,0,0)), (((blockSize * (4+x)) + xOffset), ((gameSize*blockSize) + int(blockSize * .5)) + yOffset))
		playerTiles[x] = [character,False]

def undoPlacedTiles():
	color = brown
	#redraw board
	for x in range(gameSize):
		for y in range(gameSize):
			#check if tile is due to be cleared
			if tiles[x][y][3] != None and not tiles[x][y][4] :
				#clear tile value
				tiles[x][y][3] = None
				#redraw game board
				#center
				if x==7 and y==7:
					tileColor = pink
				#double word
				elif (x,y) in doubleWords:
					tileColor = pink
				#double letter
				elif (x,y) in doubleLetters:
					tileColor = lightBlue
				#triple word
				elif (x,y) in tripleWords:
					tileColor = red
				#triple letter
				elif (x,y) in tripleLetters:
					tileColor = darkBue
				#plain square
				else:
					tileColor = beige
				pygame.draw.rect(screen, tileColor, pygame.Rect(((x*blockSize)+1),(y*blockSize),(blockSize-2),(blockSize-2)))
	#replace tiles in playerTiles
	for tile in playerTiles:
		#reset placed value
		tile[1] = False
		#redraw
		for i in range(7):
			character = playerTiles[i][0]
			xOffset = (blockSize - font.size(character)[0]) / 2
			yOffset = (blockSize - font.size(character)[1]) / 2

			pygame.draw.rect(screen, color, pygame.Rect(((blockSize * (4+i)),((gameSize*blockSize) + int(blockSize * .5)),(blockSize-2),(blockSize-2))))
			screen.blit(font.render(character, True, (0,0,0)), (((blockSize * (4+i)) + xOffset), ((gameSize*blockSize) + int(blockSize * .5)) + yOffset))

def finalizePlacedTiles():
	#check for play validity
	if not checkValidity():
		return 	#if play is invalid, halt execution of finalizing play
	#update scores
	global gameScore
	gameScore += turnScore
	updateScore(turnScore, gameScore)
	#set tiles to locked
	for x in range(gameSize):
		for y in range(gameSize):
			if tiles[x][y][3] != None:
				tiles[x][y][4] = True
	#replenish player tiles
	for index in range(len(playerTiles)):
		#don't replenish if letterbag is empty
		if len(letterBag) == 0:
			#TODO clear empty player tile slots of values
			break
		if playerTiles[index][1] == True:
			#reset player tile values
			try:
				playerTiles[index][0] = letterBag.pop()
			except:
				print "OUT OF TILES"
			playerTiles[index][1] = False
			#redraw player tile
			xOffset = (blockSize - font.size(playerTiles[index][0])[0]) / 2
			yOffset = (blockSize - font.size(playerTiles[index][0])[1]) / 2
			pygame.draw.rect(screen, brown, pygame.Rect(((blockSize * (4+index)),((gameSize*blockSize) + int(blockSize * .5)),(blockSize-2),(blockSize-2))))
			screen.blit(font.render(playerTiles[index][0], True, (0,0,0)), (((blockSize * (4+index)) + xOffset), ((gameSize*blockSize) + int(blockSize * .5)) + yOffset))
	#updated scoreboard
	updateScore(turnScore, gameScore)

def fillLetterBag():
	#unshuffled letter list
	letterBag = []
	#populate list according to official distributions
	i = 0
	for letter in string.ascii_uppercase:
		for iteration in range(letterDistributions[i]):
			letterBag.append(letter)
		i += 1
	random.shuffle(letterBag)

	return letterBag

def checkValidity():
	#iterate over all tiles and get placed tiles
	placedTiles = []
	for x in range(gameSize):
		for y in range(gameSize):
			if tiles[x][y][3] != None and not tiles[x][y][4]:
				placedTiles.append([x,y])

	#check if center tile is populated
	if tiles[7][7][3] == None:
		undoPlacedTiles()
		return False

	#check 'linearity'
	xShift = False
	yShift = False
	for tile in placedTiles:
		if placedTiles[0][0] != tile[0]:
			xShift = True
		if placedTiles[0][1] != tile[1]:
			yShift = True
	#if there is shift in both directions, it fails linearity check
	if xShift and yShift:
		undoPlacedTiles()
		return False
	

	#ensure all played tiles are connected
	if xShift:	#check L/R
		tilesConnected = True
		yIndex = placedTiles[0][1]
		for xIndex in range(placedTiles[0][0],(placedTiles[-1][0] + 1)):
			if tiles[xIndex][yIndex][3] == None:
				#if there is a blank tile between placed tiles, fails 'tiles connected' test
				undoPlacedTiles()
				return False 
	if yShift:	#check U/D
		tilesConnected = True
		xIndex = placedTiles[0][0]
		for yIndex in range(placedTiles[0][1],(placedTiles[-1][1] + 1)):
			if tiles[xIndex][yIndex][3] == None:
				#if there is a blank tile between placed tiles, fails 'tiles connected' test
				undoPlacedTiles()
				return False 

	#get list of words created by play, calculate potential score, and check that play is touching a locked tile
	includesLocked = False
	words = []	#list of all words from play
	global turnScore
	turnScore = 0
	wordMod = 0
	#get L/R words
	lastFound = []	#head of previously recorded word to avoid duplicates in list
	for tile in placedTiles:
		head = deepcopy(tile)	#deepcopy to avoid passing by reference
		while tiles[head[0]-1][head[1]][3] != None:
			if head[0] == 0:
				break
			head[0] -= 1
		if head == lastFound:	#if head is the same as previously added word, continue for loop
			continue

		#calculate word score
		turnScore += calculateScore(deepcopy(head),1)

		lastFound = deepcopy(head)	#record new head value
		word = []
		while tiles[head[0]][head[1]][3] != None:
			if tiles[head[0]][head[1]][4] == True:	#check if play is touching a locked tile
				includesLocked = True
			word.append(tiles[head[0]][head[1]][3])
			if head[0] == (gameSize - 1):
				break
			head[0] += 1
		if len(word) > 1:
			words.append(word)
	#get U/D words
	lastFound = []
	for tile in placedTiles:
		head = deepcopy(tile)
		while tiles[head[0]][head[1]-1][3] != None:
			if head[1] == 0:
				break
			head[1] -= 1
		if head == lastFound:	#if head is the same as previously added word, continue for loop
			continue

		#calculate word score
		turnScore += calculateScore(deepcopy(head),0)

		lastFound = deepcopy(head)	#record new head value
		word = []
		while tiles[head[0]][head[1]][3] != None:
			if tiles[head[0]][head[1]][4] == True:	#check if play is touching a locked tile
				includesLocked = True
			word.append(tiles[head[0]][head[1]][3])
			if head[1] == (gameSize - 1):
				break
			head[1] += 1
		if len(word) > 1:
			words.append(word)

	#if locked tile isn't found on any play but the first, invalid move
	if tiles[7][7][4] and not includesLocked:
		undoPlacedTiles()
		return False 

	#check for single letter words
	if not len(words) > 0:
		undoPlacedTiles()
		return False

	#check dictionary
	if not checkDictionary(words):
		undoPlacedTiles()
		return False

	#return true if all validation checks are passed			
	return True

def checkDictionary(words):
	#TODO more efficient search algorithm?
	for word in words:
		dictionary.seek(0)	#reset file header
		word = "".join(word).lower() + '\n'
		valid = False
		for line in dictionary:
			if line == word:
				valid = True
				break

		if not valid:
			return False

	return True

def calculateScore(head, linearity):
	def getLetterValue(letter):
		if letter in ['A','E','I','L','N','O','R','S','T','U']:
			return 1
		elif letter in ['D','G']:
			return 2
		elif letter in ['B','C','M','P']:
			return 3
		elif letter in ['F','H','V','W','Y']:
			return 4
		elif letter in ['K']:
			return 5
		elif letter in ['J','X']:
			return 8
		elif letter in ['Q','Z']:
			return 10

	wordScore = 0
	wordMod = 0
	wordSize = 0
	#linearity 1 = l/r, 0 = u/d
	if linearity:
		while tiles[head[0]][head[1]][3] != None:
			#get tile score
			wordScore += getLetterValue(tiles[head[0]][head[1]][3]) * tiles[head[0]][head[1]][2][0]
			if tiles[head[0]][head[1]][2][1] != 1:
				wordMod += tiles[head[0]][head[1]][2][1]
			if head[0] == (gameSize - 1):
				break
			wordSize += 1
			head[0] += 1
		if wordSize > 1:
			if wordMod ==0:
				wordMod = 1
			return wordScore * wordMod
		else:
			return 0
	else:
		while tiles[head[0]][head[1]][3] != None:
			#get tile score
			wordScore += getLetterValue(tiles[head[0]][head[1]][3]) * tiles[head[0]][head[1]][2][0]
			if tiles[head[0]][head[1]][2][1] != 1:
				wordMod += tiles[head[0]][head[1]][2][1]
			if head[1] == (gameSize - 1):
				break
			wordSize += 1
			head[1] += 1
		if wordSize > 1:
			if wordMod ==0:
				wordMod = 1
			return wordScore * wordMod
		else:
			return 0

def playAtRandom():
	#Random number of tiles
	random.seed()
	head = (random.randint(0,gameSize-1), random.randint(0,gameSize-1))
	placementDirection = random.randint(0,1)

	playerTilesToUse = []
	for i in range(7):
		playerTilesToUse.append(i + 1)
	random.shuffle(playerTilesToUse)

	for i in range(random.randint(0,6)):
		playerTilesToUse.pop(-1)
	# print playerTilesToUse

	j = 0
	if placementDirection:
		#place L/R
		for i in playerTilesToUse:
			try:
				placeTile((head[0] + j,head[1]), i)
				#print "Getting playerTile at index ",  i, " and placing at index (", head[0] + j, ",", head[1], ")" 
			except:
				break
			j += 1
	else:
		#place U/D
		for i in playerTilesToUse:
			try:
				placeTile((head[0],head[1] + j), i)
				#print "Getting playerTile at index ",  i, " and placing at index (", head[0] + j, ",", head[1], ")" 
			except:
				break
			j += 1

	# pygame.display.flip()
	finalizePlacedTiles()

		





#color definitions
white = (255,255,255)
beige = (253, 245, 230)
pink = (255,204,204)
red = (255,51,51)
lightBlue = (153,204,255)
darkBue = (51,153,255)
brown = (160,80,45)
red = (255,0,0)
gray = (128, 128,128)

#game parameters
gameSize = 15
blockSize = 50
letterDistributions = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1]
pointDistributions= [1,3,3,2,1,4,2,4,1,8,5,1,3,1,1,3,10,1,1,1,1,4,4,8,4,10]
dictionary = file('dictionary.txt')

#one-time initlializers
pygame.init()
done = False
selectedTile = ''
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', blockSize)
subFont = pygame.font.SysFont('Arial', blockSize / 2)
gameScore = 0
turnScore = 0

#modified tile coordinates
doubleWords = [(1,1),(2,2),(3,3),(4,4),(10,10),(11,11),(12,12),(13,13),(13,1),(12,2),(11,3),(10,4),(4,10),(3,11),(2,12),(1,13)]
doubleLetters = [(0,3),(0,11),(2,6),(2,8),(3,0),(3,7),(3,14),(6,2),(6,6),(6,8),(6,12),(7,3),(7,11),(8,2),(8,6),(8,8),(8,12),(11,0),(11,7),(11,14),(12,6),(12,8),(14,3),(14,11)]
tripleWords = [(0,0),(7,0),(14,0),(0,7),(14,7),(0,14),(7,14),(14,14)]
tripleLetters = [(1,5),(1,9),(5,1),(5,5),(5,9),(5,13),(9,1),(9,5),(9,9),(9,13),(13,5),(13,9)]

#display setup
screen = pygame.display.set_mode(((gameSize*blockSize), ((gameSize + 2)*blockSize)))
screen.fill(white)

#game setup
setupBoard()
letterBag = fillLetterBag()

#modifier standard --> (letter multiplier, word multiplier)
tiles = [[0 for x in range(gameSize)] for y in range(gameSize)]
setupTiles(tiles)

playerTiles = [0 for x in range(7)]
setupPlayerTiles()




executions = 0
#game loop
while not done:
	playAtRandom()
	executions += 1
	if executions % 100 == 0:
		print executions
		pygame.display.flip()


	# for event in pygame.event.get():
	# 	if event.type == pygame.QUIT:
	# 		done = True
	# 	if event.type == pygame.MOUSEBUTTONUP:
	# 		if selectedTile != '':
	# 			placeTile(getCoordinate(pygame.mouse.get_pos()), selectedTile)
	# 		selectedTile = selectTile(getCoordinate(pygame.mouse.get_pos()))

	# 	if event.type == pygame.KEYUP:
	# 		if event.key == pygame.K_ESCAPE:
	# 			undoPlacedTiles()
	# 		if event.key == pygame.K_RETURN:
	# 			finalizePlacedTiles()


	# pygame.display.flip()
	# clock.tick(240)