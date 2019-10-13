import pygame
import sys

#function definitions
def getCoordinate(mousePosition):
	x,y = int((float(mousePosition[0]) / float(gameSize * blockSize)) * float(gameSize)),int((float(mousePosition[1]) / float(gameSize * blockSize)) * float(gameSize)) 
	return (x,y)

def placeTile(coordinates, character):
	#update tile
	#TODO tuple problem
	#tiles[coordinates[0]][coordinates[1]][3] = character
	#repaint tile
	pygame.draw.rect(screen, brown, pygame.Rect(((coordinates[0]*blockSize)+1),(coordinates[1]*blockSize),(blockSize-2),(blockSize-2)))
	#place letter
	xOffset = (blockSize - font.size(character)[0]) / 2
	yOffset = (blockSize - font.size(character)[1]) / 2
	screen.blit(font.render(character, True, (0,0,0)), (((coordinates[0] * blockSize) + xOffset), ((coordinates[1] * blockSize)) + yOffset))


#one-time initlializers
pygame.init()
done = False
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 50)

#game parameters
gameSize = 15
blockSize = 50

#modified tile coordinates
doubleWords = [(1,1),(2,2),(3,3),(4,4),(10,10),(11,11),(12,12),(13,13),(13,1),(12,2),(11,3),(10,4),(4,10),(3,11),(2,12),(1,13)]
doubleLetters = [(0,3),(0,11),(2,6),(2,8),(3,0),(3,7),(3,14),(6,2),(6,6),(6,8),(6,12),(7,3),(7,11),(8,2),(8,6),(8,8),(8,12),(11,0),(11,7),(11,14),(12,6),(12,8),(14,3),(14,11)]
tripleWords = [(0,0),(7,0),(14,0),(0,7),(14,7),(0,14),(7,14),(14,14)]
tripleLetters = [(1,5),(1,9),(5,1),(5,5),(5,9),(5,13),(9,1),(9,5),(9,9),(9,13),(13,5),(13,9)]

#tiles
#modifier standard --> (letter multiplier, word multiplier)
tiles = [[0 for x in range(gameSize)] for y in range(gameSize)]
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
		#x coord, y coord, modifier, letter
		tiles[x][y] = (x,y,modifier,None)

#color definitions
white = (255,255,255)
beige = (253, 245, 230)
pink = (255,204,204)
red = (255,51,51)
lightBlue = (153,204,255)
darkBue = (51,153,255)
brown = (160,80,45)
gray = (128, 128,128)


#display setup
screen = pygame.display.set_mode(((gameSize*blockSize), (gameSize*blockSize)))
screen.fill(white)

#fill board with squares
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




#game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #fill selected blocks gray
        if event.type == pygame.MOUSEBUTTONUP:
			placeTile(getCoordinate(pygame.mouse.get_pos()), 'I')
			
			#print font.size('A')


    pygame.display.flip()
    clock.tick(60)