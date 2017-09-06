import pygame
import time
import random
import os.path

pygame.init()

#Global variables:
clock = pygame.time.Clock()
resourcesFolder = 'resources/'
savesFolder = resourcesFolder + 'saves/'
settingsFolder = savesFolder + 'settings/'
standardFont = 'walkwaysemibold'
lastLoopPressing = False

#Top level functions:
def getBestResulotion():
	'''Returns the best resulotion available'''
	workingResulotions = pygame.display.list_modes()
	return workingResulotions[0][0], workingResulotions[0][1]
def deleteFileContent(file):
    file.seek(0)
    file.truncate()
def checkFileExisting(file):
	'''File is path + file + sufix'''
	return os.path.isfile(file)
def setWindowProperties():
	pygame.display.set_caption("Pong")  #just the window title
	icon = pygame.image.load("resources/Icon.png") #Loads the icon 
	pygame.display.set_icon(icon)
class CreateSettings(object):
	def __init__(self, options, load):
		self.settings = options
		self.updateDisplayDimensions()
		if load == True:
			self.load()
		self.updateDisplay()
	def save(self):
		file = open(settingsFolder + 'saved_settings.txt', 'w+')
		deleteFileContent(file)
		file.write(str(self.settings))
		file.close()
	def load(self):
		if checkFileExisting(settingsFolder + 'saved_settings.txt'):
			file = open(settingsFolder + 'saved_settings.txt', 'r')
			self.savedSettings = file.read()
			try: 
				self.settings = eval(self.savedSettings)
			except Exception as e:
				print('Exeption: ' + str(e))
			self.updateDisplayDimensions()
	def updateDisplayDimensions(self):
		global displayWidth
		global displayHeight
		displayWidth = self.settings['width']
		displayHeight = self.settings['height']
	def updateDisplay(self):
		global gameDisplay
		if self.settings['fullscreen'] == True:
			gameDisplay = pygame.display.set_mode((self.settings['width'], self.settings['height']), pygame.FULLSCREEN)
		else:
			gameDisplay = pygame.display.set_mode((self.settings['width'], self.settings['height']))
displayWidth, displayHeight = getBestResulotion()
settings = CreateSettings({'width': displayWidth, 'height': displayHeight, 'VSyncStatus': True, 'VSync': 60, 'fullscreen': True}, True)
class CreateColors(object): 
	def __init__(self):
		self.white = (255,255,255)
		self.grey = (128,128,128)
		self.black = (0,0,0)
		self.red = (255,0,0)
		self.green = (0,255,0)
		self.blue = (0,0,255)
		self.d_red = (200,0,0)
		self.d_green = (0,200,0)
		self.d_blue = (0,0,200)
		self.d_Grey = (64,64,64)
		self.der_Grey = (32,32,32)
colors = CreateColors() #Colors in a class
class Button(object):
	def __init__(self, colors, dim, text, active = True):
		'''Takes a list of different colors, a list of width and height in pixels and one optional if the button is active'''	
		#[color, hoverColor, pressedColor ,inactiveColor, textColor]
		#   0       1              2             3           4
		self.colors = colors
		self.width = dim[0]
		self.height = dim[1]
		self.active = active
		self.currentColor = 0
		self.noRender = False
		self.text = text
	def updateButton(self, pos, centerd, pressedBefore = False):
		if self.active == True: #If the button is inactive, it WILL still be rendered by default but NOT collision detected
			if centerd == True:
				pos[0] -= int(self.width/2)
				pos[1] -= int(self.height/2)
			buttonPressed = False
			cursPos = pygame.mouse.get_pos()
			cursPress = pygame.mouse.get_pressed()
			global lastLoopPressing
			if rectCollision(((pos[0],pos[0] + self.width), (pos[1],pos[1] + self.height)), ((cursPos[0], cursPos[0]), (cursPos[1], cursPos[1]))):
				self.currentColor = 1 #Hovercolor set
				if lastLoopPressing == True and cursPress[0] == False:
					buttonPressed = True 
			else:
				self.currentColor = 0
			if cursPress[0] == 1:
				lastLoopPressing = True
			else: 
				lastLoopPressing = False
		else:
			self.currentColor = 3
		if self.noRender == False: #Dont render?
			if pressedBefore == True:
				self.currentColor = 2
			self.render(pos)
		return buttonPressed #Returns if key == pressed
	def render(self, pos):
		pygame.draw.rect(gameDisplay, self.colors[self.currentColor], (pos[0], pos[1], self.width, self.height))	   #    c2x1  <  c1x1   <    c2x2 or c1
		textToScreen(self.text[0], self.colors[4], self.text[1], pos[0] + self.width/2, pos[1] + self.height/2, True, self.text[2])
def rectCollision(rect1, rect2):
	# rect1/2 ~ ((x = 10, x2 = 20),(y = , y2 = 30))
	if rect2[0][0] <= rect1[0][0] <= rect2[0][1] or rect2[0][0] <= rect1[0][1] <= rect2[0][1] or rect1[0][0] <= rect2[0][0] <= rect1[0][1] or rect1[0][0] <= rect2[0][1] <= rect1[0][1]: #x1
		if rect2[1][0] <= rect1[1][0] <= rect2[1][1] or rect2[1][0] <= rect1[1][1] <= rect2[1][1] or rect1[1][0] <= rect2[1][0] <= rect1[1][1] or rect1[1][0] <= rect2[1][1] <= rect1[1][1]:
			return True
	else:
		return False
def updateTimeMultipiler(preClock):
	clock = time.clock()
	return clock - preClock, clock
def textObject(text, color, size = 25, font = standardFont):
	textSurface = pygame.font.SysFont(font, size).render(text, True, color)
	return textSurface, textSurface.get_rect()
def textToScreen(text, color, size, xCord, yCord, centreOnCordinates, font):

	textSurf, textRect = textObject(text, color, size, font)
	if centreOnCordinates == True:
		textRect.center = (xCord, yCord)
	else:
		textRect = (xCord, yCord)
	gameDisplay.blit(textSurf, textRect)
def updatePaddlePosition(paddleHeight):
	'''Makes sure that the paddle doesen't leave the screen'''
	mouseYPos = pygame.mouse.get_pos()[1]
	if mouseYPos + paddleHeight/2 > displayHeight:
		pos = displayHeight - paddleHeight
	elif mouseYPos - paddleHeight/2 < 0:
		pos = 0
	else:
		pos = mouseYPos - paddleHeight/2
	return pos
def rectMesh(cord, width, height):
	x1 = cord[0]
	x2 = cord[0] + width
	y1 = cord[1]
	y2 = cord[1] + height
	return ((x1,x2),(y1,y2))
def ballMovment(speed, direction, prevCordinate, multipiler):
	cordinates = []
	if direction[0] == 'LEFT':
		cordinates.append(prevCordinate[0] - speed[0] * multipiler)

	elif direction[0] == 'RIGHT':
		cordinates.append(prevCordinate[0] + speed[0] * multipiler)
	if direction[1] == 'UP':
		cordinates.append(prevCordinate[1] - speed[1] * multipiler)
	elif direction[1] == 'DOWN':
		cordinates.append(prevCordinate[1] + speed[1] * multipiler)
	return cordinates
def createBall(x, y, direction, radius, movment, color = [0,0,0]):
	return {'cords': [x, y], 'direction': direction, 'hitted': False, 'radius': radius, 'movment': movment, 'mesh': False, 'color': color}
def randomGrey(min, max):
	g = random.randint(min ,max)
	return[g,g,g]
def waveBall(paddleHeight):
	radius = int(random.randint(int(paddleHeight/8),  int(paddleHeight)))
	x = random.randint(int(displayWidth), int(displayWidth * 2))
	y = random.randint(int(0 + radius) ,int(displayHeight - radius))
	direction = []
	direction.append('LEFT')
	direction.append(random.choice(['UP', 'DOWN']))
	movment = []
	movment.append(random.randint(displayWidth/4 ,displayWidth/1))
	movment.append(random.randint(0 ,displayHeight/1.5))
	color = randomGrey(100, 255)
	return createBall(x, y, direction, radius, movment, color)
def ballMesh(cord, radius):
	x1 = cord[0] - radius
	x2 = cord[0] + radius
	y1 = cord[1] - radius
	y2 = cord[1] + radius
	return ((x1, x2),(y1, y2))
def mainLoop():
	#scoop variables:
	loopExit = False
	preClock = time.clock() #Used to change the movment depending on the FPS
	activeLoops = {'gameIntro': True, 'pause': False, 'game': False, 'FPSMeter': True, 'modesScreen': False, 'pause': False}
	background = colors.black
	buttonFontSize = 25
	buttonColorScheme = (colors.white,colors.grey,colors.der_Grey,colors.red, colors.black)
	buttonDim = [125,50]
	startButton = Button(buttonColorScheme, buttonDim, ('START', buttonFontSize, standardFont))
	optionsButton = Button(buttonColorScheme, buttonDim, ('OPTIONS', buttonFontSize, standardFont))
	exitButton = Button(buttonColorScheme, buttonDim, ('EXIT', buttonFontSize, standardFont))
	continueButton = Button(buttonColorScheme, buttonDim, ('CONTINUE', buttonFontSize, standardFont))
	score = 0
	#Start of the loops:
	while  not loopExit:
		keys = pygame.key.get_pressed()
		timeMultipiler, preClock = updateTimeMultipiler(preClock) #Updates the variable that controls the movment per second
		gameDisplay.fill(background)
		noRender = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		if activeLoops['gameIntro']: #Game intro loop
			textToScreen("PONG", colors.white, int(displayHeight/5), int(displayWidth/2), int(displayHeight/4), True, standardFont)
			if startButton.updateButton([int(displayWidth/2), int(displayHeight/2)], True):
				activeLoops['gameIntro'] = False
				activeLoops['modesScreen'] = True
				wavesButton = Button(buttonColorScheme, buttonDim, ('DEFEND', buttonFontSize, standardFont))
				noRender = True
			if optionsButton.updateButton([int(displayWidth/2), int(displayHeight/2 + buttonDim[1] * 2)], True):
				pass
			if exitButton.updateButton([int(displayWidth/2), int(displayHeight/2 + buttonDim[1] * 4)], True):
				pygame.quit()
				quit()
		if activeLoops['modesScreen'] and noRender == False:
			if wavesButton.updateButton([int(displayWidth/2), int(displayHeight/2)], True):
				gamemode = 'DEFEND'
				paddleWidth =  int(displayWidth/100)
				paddleHeight = int(displayHeight/10)
				paddleX = displayWidth/20
				balls = [waveBall(paddleHeight)]#[createBall(displayWidth/0.9, displayHeight/2, ['LEFT','DOWN'], paddleHeight/2, [displayWidth/2, displayHeight/2])]
				print(balls[0])
				upperWall = rectMesh((0, 0), displayWidth * 2, 0)
				lowerWall = rectMesh((0, displayHeight), displayWidth * 2, 0)
				sideWall = rectMesh((displayWidth, 0), 0, displayHeight)
				score = 0
				activeLoops['modesScreen'] = False
				activeLoops['game'] = True
				noRender = True
		if activeLoops['game'] and noRender == False: #Game loop
			if keys[pygame.K_ESCAPE]:  
				noRender = True
				activeLoops['pause'] = True
				activeLoops['game'] = False
			paddleY = updatePaddlePosition(paddleHeight)
			paddleMesh = rectMesh((paddleX, paddleY), paddleWidth, paddleHeight)
			pygame.draw.rect(gameDisplay, colors.white, (paddleX, paddleY, paddleWidth, paddleHeight))
			textToScreen("SCORE:" + str(score), colors.white, int(displayHeight/60), 0, 0, False, standardFont)
			for i in balls:
				ball = balls.index(i) #ball is the index of the current ball in balls
				balls[ball]['cords'] = ballMovment(balls[ball]['movment'], balls[ball]['direction'], balls[ball]['cords'], timeMultipiler)
				balls[ball]['mesh'] = ballMesh(balls[ball]['cords'], balls[ball]['radius'])
				#Not using i because I have to update balls[i] and then the data refrenced to i will not be up to date
				#There are occasions where it's possible to use i.
				if rectCollision(paddleMesh, balls[ball]['mesh']):
					balls[ball]['direction'][0] = 'RIGHT'
					score += 1
					if balls[ball]['hitted'] == False:
						balls.append(waveBall(paddleHeight))
					balls[ball]['hitted'] = True
				if rectCollision(lowerWall, balls[ball]['mesh']):
					balls[ball]['direction'][1] = 'UP'
				if rectCollision(upperWall, balls[ball]['mesh']):
					balls[ball]['direction'][1] = 'DOWN'
				if balls[ball]['cords'][0] > displayWidth + balls[ball]['radius'] and balls[ball]['hitted'] == True:
					balls.pop(ball) #Removes the ball that just flew away
				pygame.draw.circle(gameDisplay, balls[ball]['color'], (int(balls[ball]['cords'][0]),int(balls[ball]['cords'][1])), int(balls[ball]['radius']))
		if activeLoops['pause'] and noRender == False:
			if keys[pygame.K_ESCAPE]:  
				noRender = True
				activeLoops['pause'] = False
				activeLoops['game'] = True
			if continueButton.updateButton([int(displayWidth/2), int(displayHeight/2)], True):
				activeLoops['pause'] = False
				activeLoops['game'] = True
			textToScreen("PAUSED", colors.white, 40, int(displayWidth/2), int(displayHeight/4), True, standardFont)
		if activeLoops['FPSMeter']: #FPS loop
			pass
			#print('FPS: ' + str(clock.get_fps()))
		pygame.display.update() #Updates VSync times per second
		pygame.event.clear()
		if settings.settings['VSyncStatus'] == True:
			clock.tick(settings.settings['VSync']) #Used as a V-Sync feature
setWindowProperties()
mainLoop()