#!/usr/bin/env python
#Team Members:
#Anna Nicole Tupas, anicole_tupas@csu.fullerton.edu, CWID 890827272
#Elizabeth Nguyen, syaora@csu.fullerton.edu, CWID 893150359
#Kristi Chang, kristi.chang@csu.fullerton.edu, CWID 891162851
#This program is an infinite runner where the player is the bunny

import pygame
import random, sys

pygame.init()

font = "Sniglet-ExtraBold.otf"

#Game Initialization
pygame.init()

#Game Resolution
screen_width = 800
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))

#Text Renderer
def text_format(message, textFont, textSize, textColor):
	newFont = pygame.font.Font(textFont, textSize)
	newText = newFont.render(message, 0, textColor)
	return newText

#Colors
white = (219, 219, 219)
black = (0,255,0)
green = (0,100,0)
yellow = (0,255,0)
beige = (245, 222, 179)

#Global Variable
boxsize = 75
gapsize = 10
xmargin = int((screen_width - (3 * (boxsize + gapsize))) / 2)
ymargin = int((screen_height - (6 * (boxsize + gapsize))) / 2)

forest = pygame.image.load('forest.png')
carrot = pygame.image.load('carrot.png')
bunny = pygame.image.load('player.png')
pygame.display.set_icon(bunny)

rock = pygame.image.load('rock.png')
forest = pygame.transform.scale(forest, (800, 500))
x = 0


#Game Framerate
clock = pygame.time.Clock()
FPS = 30

def leftTopCoordsOfBox(boxx, boxy):
	left = boxx * (boxsize + gapsize) + xmargin
	top = boxy * (boxsize + gapsize) + ymargin
	return (left, top)

def drawBoard(board):
	half = int(boxsize * 0.5)
	temp = []
	
	#Flip the array upside down so that it could be displayed correctly
	for x in range(3):
		column = []
		for y in reversed(range(6)):
			column.append(board[x][y])
		temp.append(column)

	#Draw the board at its current state
	for boxx in range(3):
		for boxy in range(6):
			left, top = leftTopCoordsOfBox(boxx, boxy)
			pygame.draw.rect(screen, beige, (left, top, boxsize, boxsize))
			if temp[boxx][boxy] == "c":
				screen.blit(carrot, (left + int(boxsize * 0.1), top + int(boxsize * 0.1), boxsize - half, boxsize - half))
			elif temp[boxx][boxy] == "r":
				screen.blit(rock, (left + int(boxsize * 0.1), top + int(boxsize * 0.1), boxsize - half, boxsize - half))
			elif temp[boxx][boxy] == "p":
				screen.blit(bunny, (left + int(boxsize * 0.1), top + int(boxsize * 0.1), boxsize - half, boxsize - half))

def createNewRow(board, moveCount, speed):
	new_row = ["s", "s", "s", "s"]
	rand_num = random.randint(0, 100)
	if moveCount % (2 * speed) == 0:
		rand_rock = random.randint(0, 3)
		new_row[rand_rock] = "r"
	if rand_num <= 30:
		rand_num = random.randint(0, 3)
		if new_row[rand_num] == "r":
			rand_num = abs(rand_num - random.randint(1, 3))
		new_row[rand_num] = "c"

	newBoard = []
	for x in range(3):
		column = []
		for y in range(6):
			if y == 5:
				column.append(new_row[x])
			else:
				column.append(board[x][y+1])
		newBoard.append(column)

	return newBoard

#Game
def gameLoop():
	moveCount = 0
	board = []
	playerPos = 1 #Keeps track on where the player is (0 being the left, 1 middle, 2 right)
	carrots = 0
	speed = 10
	scoreValue = 0

	crash = False
	for x in range(3):
		column = []
		for y in range(6):
			column.append("s")
		board.append(column)
	board[playerPos][0] = "p" 
	
	while True:
		#Background setup
		rel_y = y % forest.get_rect().height
		
		screen.blit(forest, (0, rel_y - forest.get_rect().height))
		if rel_y < screen_height:
			screen.blit(forest, (0, rel_y))
		y -= -5

		#Score Text
		scoreValue = moveCount + (20 * carrots)
		score = text_format("Score: %r" % scoreValue, font, 20, yellow)
		score_rect = score.get_rect()
		screen.blit(score, (10, 10))
		
		carrotText = text_format("Carrots: %r" % carrots, font, 20, yellow)
		carrot_rect = carrotText.get_rect()
		screen.blit(carrotText, (10, 30))

		#Board setup
		crash = hasCollided(board[playerPos][0])
		carrots += hasCarrots(board[playerPos][0])
		
		board[playerPos][0] = "p"
		drawBoard(board)
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					board[playerPos][0] = "s"
					if playerPos == 0:
						playerPos = 1
					else:
						playerPos = 2
					#crash = hasCollided(board[playerPos][0])
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					board[playerPos][0] = "s"
					if playerPos == 2:
						playerPos = 1
					else:
						playerPos = 0
					#crash = hasCollided(board[playerPos][0])

		if crash:
			gameOver(scoreValue, carrots)
		
		#Handles the speed of the game
		if moveCount > 100:
			speed = 9
		if moveCount > 500:
			speed = 7
		if moveCount > 1000:
			speed = 5
		if moveCount > 2000:
			speed = 3
		if moveCount > 3000:
			speed = 2

		moveCount+= 1
		if moveCount % speed == 0:
			board = createNewRow(board, moveCount, speed)
		clock.tick(FPS)

def hasCollided(value):
	if value == "r":
		return True
	return False

def hasCarrots(value):
	if value == "c":
		return 1
	return 0

#How to Play
def howto():

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						main_menu()

		#Main Menu UI
		screen.fill(green)
		title = text_format("HOW TO PLAY", font, 90, yellow)
		title_rect = title.get_rect()		
		screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))

		howto1 = text_format("Play as a bunny in a forest."	, font, 30, white)
		howto2 = text_format("Pick up carrots and dodge rocks."	, font, 30, white)
		howto3 = text_format("Use the left and right arrows to move."	, font, 30, white)
		howto4 = text_format("The game will speed up as it goes on."	, font, 30, white)
		howto5 = text_format("press [enter] to go back"	, font, 30, white)
		
		screen.blit(howto1, (80, 190))
		screen.blit(howto2, (80, 250))
		screen.blit(howto3, (80, 310))
		screen.blit(howto4, (80, 370))
		screen.blit(howto5, (80, 430))		


		pygame.display.set_caption("How to Play")
		pygame.display.update()
		clock.tick(FPS)

#Game Over
def gameOver(moveCount, carrotCount):
	selected = "playagain"

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					if selected == "mainmenu":
						selected = "playagain"
					elif selected == "quit":
						selected = "mainmenu"
				elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
					if selected == "playagain":
						selected = "mainmenu"
					elif selected == "mainmenu":
						selected = "quit"
				if event.key == pygame.K_RETURN:
					if selected == "playagain":
						clock.tick(FPS)
						gameLoop()
					if selected == "mainmenu":
						clock.tick(FPS)
						main_menu()
					if selected == "quit":
						pygame.quit()
						quit()
		
		#Main Menu UI
		screen.fill(green)
		title = text_format("Game Over", font, 90, yellow)
		score = text_format("Score: %r" % moveCount, font, 50, yellow)
		carrotText = text_format("Carrots: %r" % carrotCount, font, 50, yellow)


		if selected == "playagain":
			text_playagain = text_format("PLAY AGAIN", font, 40, black)
		else:
			text_playagain = text_format("PLAY AGAIN", font, 40, white)
		if selected == "mainmenu":
			text_mainmenu = text_format("MAIN MENU", font, 40, black)
		else:
			text_mainmenu = text_format("MAIN MENU", font, 40, white)
		if selected == "quit":
			text_quit = text_format("QUIT", font, 40, black)
		else:
			text_quit = text_format("QUIT", font, 40, white)

		title_rect = title.get_rect()
		score_rect = score.get_rect()
		carrot_rect = carrotText.get_rect()
		playagain_rect = text_playagain.get_rect()
		mainmenu_rect = text_mainmenu.get_rect()
		quit_rect = text_quit.get_rect()

		#Main Menu Text
		screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
		screen.blit(score, (screen_width/2 - (score_rect[2]/2), 160))
		screen.blit(carrotText, (screen_width/2 - (carrot_rect[2]/2), 200))
		screen.blit(text_playagain, (screen_width/2 - (playagain_rect[2]/2), 300))
		screen.blit(text_mainmenu, (screen_width/2 - (mainmenu_rect[2]/2), 360))
		screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 420))
		pygame.display.update()
		clock.tick(FPS)

#Main Menu
def main_menu():
	menu = True
	selected = "start"

	while menu:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					if selected == "quit":
						selected = "howtoplay"
					else:
						selected = "start"
				elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
					if selected == "start":
						selected = "howtoplay"
					else:
						selected = "quit"
				if event.key == pygame.K_RETURN:
					if selected == "start":
						print("Start")
						clock.tick(FPS)
						gameLoop()
					if selected == "howtoplay":
						print("howtoplay")
						clock.tick(FPS)
						howto()
					if selected == "quit":
						pygame.quit()
						quit()
		
		#Main Menu UI
		screen.fill(green)
		title = text_format("Bun Run", font, 90, yellow)
		if selected == "start":
			text_start = text_format("START", font, 40, black)
		else:
			text_start = text_format("START", font, 40, white)
		if selected == "howtoplay":
			text_howtoplay = text_format("HOW TO PLAY", font, 40, black)
		else:
			text_howtoplay = text_format("HOW TO PLAY", font, 40, white)
		if selected == "quit":
			text_quit = text_format("QUIT", font, 40, black)
		else:
			text_quit = text_format("QUIT", font, 40, white)

		title_rect = title.get_rect()
		start_rect = text_start.get_rect()
		howtoplay_rect = text_howtoplay.get_rect()
		quit_rect = text_quit.get_rect()

		by1 = text_format("By Elizabeth Nguyen, Anna", font, 30, white)
		by2 = text_format("Nicole Tupas, Kristi Chang", font, 30, white)
		by1_rect = by1.get_rect()
		by2_rect = by2.get_rect()
		screen.blit(by1, (screen_width/2 - (by1_rect[2]/2), 190))
		screen.blit(by2, (screen_width/2 - (by2_rect[2]/2), 230))

		#Main Menu Text
		screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
		screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
		screen.blit(text_howtoplay, (screen_width/2 - (howtoplay_rect[2]/2), 360))
		screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 420))
		pygame.display.update()
		clock.tick(FPS)

#Initialize the Game
if __name__ == '__main__':
	main_menu()
	pygame.quit()
	quit()
		



