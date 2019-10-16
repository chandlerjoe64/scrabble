import pygame
import string
import random
from copy import deepcopy

#TODOS
#checking for play validity before finalizing turn
#calculating points of turns
#implement blank tiles
#handle empty letter bag on player tile draws
#add text for multiplier squares
#swap tiles
#implement second player
#implement game-over when out of tiles or out of plays


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
			playerTiles[index][0] = letterBag.pop()
			playerTiles[index][1] = False
			#redraw player tile
			xOffset = (blockSize - font.size(playerTiles[index][0])[0]) / 2
			yOffset = (blockSize - font.size(playerTiles[index][0])[1]) / 2
			pygame.draw.rect(screen, brown, pygame.Rect(((blockSize * (4+index)),((gameSize*blockSize) + int(blockSize * .5)),(blockSize-2),(blockSize-2))))
			screen.blit(font.render(playerTiles[index][0], True, (0,0,0)), (((blockSize * (4+index)) + xOffset), ((gameSize*blockSize) + int(blockSize * .5)) + yOffset))

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
	#rules
	#new tiles connected
	#in dictionary
	#left/right, top/bottom
	

	#iterate over all tiles and get placed tiles
	placedTiles = []
	for x in range(gameSize):
		for y in range(gameSize):
			if tiles[x][y][3] != None and not tiles[x][y][4]:
				placedTiles.append([x,y])

	#check if center tile is populated
	if tiles[7][7][3] == None:
		print "first play"
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

	#get list of words created by play, and check that play is touching a locked tile
	#get L/R words
	includesLocked = False
	words = []	#list of all words from play
	lastFound = []	#head of previously recorded word to avoid duplicates in list
	for tile in placedTiles:
		head = deepcopy(tile)	#deepcopy to avoid passing by reference
		while tiles[head[0]-1][head[1]][3] != None:
			if head[0] == 0:
				break
			head[0] -= 1
		if head == lastFound:	#if head is the same as previously added word, continue for loop
			continue
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

	#print all words from play
	print words

	#return true if all validation checks are passed			
	return True







#one-time initlializers
pygame.init()
done = False
selectedTile = ''
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 50)

#color definitions
white = (255,255,255)
beige = (253, 245, 230)
pink = (255,204,204)
red = (255,51,51)
lightBlue = (153,204,255)
darkBue = (51,153,255)
brown = (160,80,45)
gray = (128, 128,128)

#game parameters
gameSize = 15
blockSize = 50
letterDistributions = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1]
pointDistributions= [1,3,3,2,1,4,2,4,1,8,5,1,3,1,1,3,10,1,1,1,1,4,4,8,4,10]

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




#scratch work before moving to functions





#game loop
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.MOUSEBUTTONUP:
			if selectedTile != '':
				placeTile(getCoordinate(pygame.mouse.get_pos()), selectedTile)
			selectedTile = selectTile(getCoordinate(pygame.mouse.get_pos()))

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_ESCAPE:
				undoPlacedTiles()
			if event.key == pygame.K_RETURN:
				finalizePlacedTiles()


	pygame.display.flip()
	clock.tick(60)