import pygame
import string
import random

#function definitions
def getCoordinate(mousePosition):
	#convert mouse coordinates into gameboard coordinates
	x,y = int((float(mousePosition[0]) / float(gameSize * blockSize)) * float(gameSize)),int((float(mousePosition[1]) / float(gameSize * blockSize)) * float(gameSize)) 
	return (x,y)

def placeTile(coordinates, character):
	#check if cursor is in valid location for placement
	if coordinates[1] > (gameSize - 1):
		return
	#check if tile is already populated
	if tiles[coordinates[0]][coordinates[1]][3] != None:
		return
	#update tile
	tiles[coordinates[0]][coordinates[1]][3] = selectedTile
	#repaint tile
	pygame.draw.rect(screen, brown, pygame.Rect(((coordinates[0]*blockSize)+1),(coordinates[1]*blockSize),(blockSize-2),(blockSize-2)))
	#place letter
	xOffset = (blockSize - font.size(character)[0]) / 2
	yOffset = (blockSize - font.size(character)[1]) / 2
	screen.blit(font.render(character, True, (0,0,0)), (((coordinates[0] * blockSize) + xOffset), ((coordinates[1] * blockSize)) + yOffset))
	#gray out placed player tiles
	pygame.draw.rect(screen, gray, pygame.Rect(((blockSize * (4+selectedTile)),((gameSize*blockSize) + int(blockSize * .5)),(blockSize-2),(blockSize-2))))

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
		character = random.choice(string.ascii_uppercase)
		xOffset = (blockSize - font.size(character)[0]) / 2
		yOffset = (blockSize - font.size(character)[1]) / 2

		pygame.draw.rect(screen, color, pygame.Rect(((blockSize * (4+x)),((gameSize*blockSize) + int(blockSize * .5)),(blockSize-2),(blockSize-2))))
		screen.blit(font.render(character, True, (0,0,0)), (((blockSize * (4+x)) + xOffset), ((gameSize*blockSize) + int(blockSize * .5)) + yOffset))
		playerTiles[x] = character

def undoPlacedTiles():
	color = brown
	#redraw board
	for x in range(gameSize):
		for y in range(gameSize):
			#check if tile is due to be cleared
			if tiles[x][y][3] != '' and not tiles[x][y][4] :
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
			character = playerTiles[i]
			xOffset = (blockSize - font.size(character)[0]) / 2
			yOffset = (blockSize - font.size(character)[1]) / 2

			pygame.draw.rect(screen, color, pygame.Rect(((blockSize * (4+i)),((gameSize*blockSize) + int(blockSize * .5)),(blockSize-2),(blockSize-2))))
			screen.blit(font.render(character, True, (0,0,0)), (((blockSize * (4+i)) + xOffset), ((gameSize*blockSize) + int(blockSize * .5)) + yOffset))





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

#modified tile coordinates
doubleWords = [(1,1),(2,2),(3,3),(4,4),(10,10),(11,11),(12,12),(13,13),(13,1),(12,2),(11,3),(10,4),(4,10),(3,11),(2,12),(1,13)]
doubleLetters = [(0,3),(0,11),(2,6),(2,8),(3,0),(3,7),(3,14),(6,2),(6,6),(6,8),(6,12),(7,3),(7,11),(8,2),(8,6),(8,8),(8,12),(11,0),(11,7),(11,14),(12,6),(12,8),(14,3),(14,11)]
tripleWords = [(0,0),(7,0),(14,0),(0,7),(14,7),(0,14),(7,14),(14,14)]
tripleLetters = [(1,5),(1,9),(5,1),(5,5),(5,9),(5,13),(9,1),(9,5),(9,9),(9,13),(13,5),(13,9)]

#display setup
screen = pygame.display.set_mode(((gameSize*blockSize), ((gameSize + 2)*blockSize)))
screen.fill(white)

#tiles
#modifier standard --> (letter multiplier, word multiplier)
tiles = [[0 for x in range(gameSize)] for y in range(gameSize)]
setupTiles(tiles)

playerTiles = [0 for x in range(7)]
setupPlayerTiles()

#game setup
setupBoard()




#scratch work before moving to functions





#game loop
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.MOUSEBUTTONUP:
			if selectedTile != '':
				placeTile(getCoordinate(pygame.mouse.get_pos()), playerTiles[selectedTile])
			selectedTile = selectTile(getCoordinate(pygame.mouse.get_pos()))

		if event.type == pygame.KEYUP:
			undoPlacedTiles()


	pygame.display.flip()
	clock.tick(60)