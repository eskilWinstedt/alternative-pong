import pygame
import time
import random
import os.path
import math

'''
Continue with making a function that can update all buttons dimensions. Use a for loop on
allButtons. 
'''
pygame.init()

#Global variables:
clock = pygame.time.Clock()
resourcesFolder = 'resources/'
savesFolder = resourcesFolder + 'saves/'
settingsFolder = savesFolder + 'settings/'
standardFont = 'walkwaysemibold'
allButtons = []

#Top level functions:
def getBestResolution():
	'''Returns the best resolution available'''
	workingResulotions = pygame.display.list_modes()
	return workingResulotions[0][0], workingResulotions[0][1]
def deleteFileContent(file):
    file.seek(0)
    file.truncate()
def checkFileExisting(file):
	'''File is path + file + .filetype'''
	return os.path.isfile(file)
def setWindowProperties():
	pygame.display.set_caption("Pong")  #just the window title
	icon = pygame.image.load("resources/Icon.png") #Loads the icon 
	pygame.display.set_icon(icon)
class CreateSettings(object):
	def __init__(self, load):
		if load == True:
			noSaved = self.loadSettings()
			if noSaved == True:
				self.detect()
		else:
			self.detect()
		self.updateDisplayDimensions() #Updates the displayHeight/displayWidth variables. This was ment to be removed :( but I forgot it 
		self.updateDisplay() #Sets fullscreen or not and resolution
	def save(self):
		file = open(settingsFolder + 'saved_settings.txt', 'w+')
		deleteFileContent(file)
		file.write(str(self.settings))
		file.close()
	def loadSettings(self):
		if checkFileExisting(settingsFolder + 'saved_settings.txt'):
			file = open(settingsFolder + 'saved_settings.txt', 'r')
			self.savedSettings = file.read()
			try: 
				self.settings = eval(self.savedSettings)
			except Exception as e:
				print('Exeption: ' + str(e))
			self.updateDisplayDimensions()
		else:
			return True
	def detect(self):
		width, height = getBestResolution()
		self.settings = {'width': width, 'height': height, 'VSyncStatus': False, 'VSync': 144, 'fullscreen': True}
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
settings = CreateSettings(True) #Setting the settings and updates the screeen. Trying to read from saved settings file. 
class CreateColors(object): 
	def __init__(self):
		self.white = (255,255,255)
		self.grey = (128,128,128)
		self.black = (0,0,0)
		self.red = (255,0,0)
		self.green = (0,255,0)
		self.blue = (0,0,255)
		self.d_red = (150,0,0)
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
		allButtons.append(self)
		self.colors = colors
		self.width = dim[0]
		self.height = dim[1]
		self.active = active
		self.currentColor = 0
		self.noRender = False
		self.text = text
		self.lastLoopPressing = False
	def updateButton(self, pos, centerd, pressedBefore = False):
		if self.active == True: #If the button is inactive, it WILL still be rendered by default but NOT collision detected
			if centerd == True:
				pos[0] -= int(self.width/2)
				pos[1] -= int(self.height/2)
			buttonPressed = False
			cursPos = pygame.mouse.get_pos()
			cursPress = pygame.mouse.get_pressed()
			if rectCollision(((pos[0],pos[0] + self.width), (pos[1],pos[1] + self.height)), ((cursPos[0], cursPos[0]), (cursPos[1], cursPos[1]))):
				self.currentColor = 1 #Hovercolor set
				if self.lastLoopPressing == True and cursPress[0] == False:  # Button pressed on mousebutton release
					buttonPressed = True 
			else:
				self.currentColor = 0 #
			if cursPress[0] == 1: #If mousebutton is pressed this loop and realeased next, buttonePressed = True
				self.lastLoopPressing = True
			else: 
				self.lastLoopPressing = False
		else:
			self.currentColor = 3  #Inactive color
		if self.noRender == False: #Dont render? USEFUL when you want to make anything to a button
			if pressedBefore == True:  #Like when a link is purple, you have already pressed it. 
				self.currentColor = 2   #Pressed before color
			self.render(pos)   
		return buttonPressed #Returns if key == pressed
	def render(self, pos):
		pygame.draw.rect(gameDisplay, self.colors[self.currentColor], (pos[0], pos[1], self.width, self.height))	   #    c2x1  <  c1x1   <    c2x2 or c1
		textToScreen(self.text[0], self.colors[4], self.text[1], pos[0] + self.width/2, pos[1] + self.height/2, True, self.text[2])
def setType(value):
	integers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	print(str(type(value)) + value)
	if integers in value[0]:
		if '.' in value:
			value = float(value)
		else:
			value = int(value)
	elif value == 'False':
		value = False
	elif value == 'True':
		value = True
	elif value[0] == "{" or "[" or "(":
		print('Warning: Possible invalid syntax in design.txt: unsuported data type. Saved as str')
	return value
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
def shrinkAnimation():
	'''A function that is going to count a spesific animation frame and return a scale value fitting the current frame. 
	args: OSize LSize speed animationType['shrinking', 'shrinking with faster and faster or less and less speed, popping, larger scale and the shrink']'''
	pass
def loadDesign():
	if checkFileExisting(resourcesFolder + 'design.txt'):
		dict = {}
		content = open(resourcesFolder + 'design.txt', 'r').read()
		keyMarker = 0
		for line in content.split('\n'):
			valueMarker = line.find(':')
			key = line[:valueMarker]
			if key == 'Tutorial': continue #If it is the tutorial line
			value = line[valueMarker + 2:]
			dict[key] = int(value)
	else:
		print('WARNING: Missing file design.txt')
		pygame.quit()
		quit()
	parts = 10000
	for key, value in list(dict.items()):
		if 'height' in key.lower() or 'y' in key.lower():
			axle = settings.settings['height']
		elif 'width' in key.lower() or 'x' in key.lower():
			axle = settings.settings['width']
		fraction = value/parts #how much of parts?
		dict[key] = int(fraction * axle)  #Transforms the fraction of parts value to fraction of displayWidth/displayHeight. Converted to int because there is only whole pixels
	return dict
def livesToScreen(score):
	'''Draws as many lives as balls. The balls are red and should be animated decreasing in size when lost. 
	animSpeed
	placement x, y, centred or not
	DistanceBetween 
	radius
	color 
	
	
	'''
	radius = int(displayHeight/60/2)
	color = colors.d_red
	
	xOffset = 1
	yOffset = 1
	
	xPos = displayWidth - radius - xOffset
	yPos = yOffset + radius 
	
	spaceBetween = radius * 3
	for i in range(score):
		pygame.draw.circle(gameDisplay, color, (xPos, yPos), radius)
		xPos -= spaceBetween
	pass
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
	return {'cords': [x, y], 'direction': direction, 'hitted': False, 'lost': False, 'radius': radius, 'movment': movment, 'mesh': False, 'color': color, 'poped': False}
def randomGrey(min, max):
	g = random.randint(min ,max)
	return[g,g,g]
def waveBall(paddleHeight):
	radius = int(random.randint(int(paddleHeight/8),  int(paddleHeight/3)))
	x = random.randint(int(displayWidth), int(displayWidth * 2))
	y = random.randint(int(0 + radius) ,int(displayHeight - radius))
	direction = []
	direction.append('LEFT')
	direction.append(random.choice(['UP', 'DOWN']))
	movment = []
	movment.append(random.randint(displayWidth/3 ,displayWidth/1))
	movment.append(random.randint(0 ,displayHeight/1.5))
	color = randomGrey(100, 255)
	return createBall(x, y, direction, radius, movment, color)
def ballMesh(cord, radius):
	x1 = cord[0] - radius
	x2 = cord[0] + radius
	y1 = cord[1] - radius
	y2 = cord[1] + radius
	return ((x1, x2),(y1, y2))
def createGameData():
	data = {
	'gamemode': 'DEFEND',
	'paddleWidth': int(displayWidth/100),
	'paddleHeight': int(displayHeight/10),
	'paddleX': displayWidth/20,
	'paddleY': 0,
	'upperWall': rectMesh((0, 0), displayWidth * 2, 0),
	'lowerWall': rectMesh((0, displayHeight), displayWidth * 2, 0),
	'sideWall': rectMesh((displayWidth, 0), 0, displayHeight),
	'lostBallBorder': rectMesh((0,0), 0, displayHeight),
	'lives': 2,
	'score': 0,
	'escPressed': False,
	'pausedAt': False,
	'continueAcceleration': 3,
	'playingGame': True,
	'gameOver':   False}
	data['balls'] = [waveBall(data['paddleHeight'])]
	return data
def mainLoop():
	dim = loadDesign()
	loopExit = False
	preClock = time.clock() #Used to change the movment depending on the FPS
	activeLoops = {'gameIntro': True, 'pause': False, 'game': False, 'FPSMeter': True, 'modesScreen': False, 'pause': False}
	background = colors.black
	buttonFontSize = 25
	buttonColorScheme = (colors.white,colors.grey,colors.der_Grey,colors.red, colors.black)
	buttonDim = [dim['button_width'], dim['button_height']]
	startButton = Button(buttonColorScheme, buttonDim, ('START', buttonFontSize, standardFont))
	optionsButton = Button(buttonColorScheme, buttonDim, ('OPTIONS', buttonFontSize, standardFont))
	exitButton = Button(buttonColorScheme, buttonDim, ('EXIT', buttonFontSize, standardFont))
	continueButton = Button(buttonColorScheme, buttonDim, ('CONTINUE', buttonFontSize, standardFont))
	restartButton = Button(buttonColorScheme, buttonDim, ('RESTART', buttonFontSize, standardFont))
	score = 0
	center = (displayWidth/2, displayHeight/2)
	#Start of the loops:
	while  not loopExit:
		frameTime = time.clock()
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
				GD =  createGameData()
				activeLoops['modesScreen'] = False
				activeLoops['game'] = True
				noRender = True
		if activeLoops['game'] and noRender == False: #Game loop
			if not GD['playingGame'] == True:
				if GD['gameOver'] == True:
					textToScreen("GAME OVER", colors.white, int(displayHeight/30), displayWidth/2, displayHeight/4, True, standardFont)
					if restartButton.updateButton([int(displayWidth/2), int(displayHeight/2)], True):
						GD = createGameData()
			else:
				if GD['pausedAt']:
					GD['pausedSince'] = frameTime - GD['pausedAt']
					if GD['pausedSince'] <= GD['continueAcceleration']:
						timeMultipiler = (GD['pausedSince']/GD['continueAcceleration']) * timeMultipiler
					else:
						GD['pausedAt'] = False
				if keys[pygame.K_ESCAPE] and GD['escPressed'] == False:  
					noRender = True
					activeLoops['pause'] = True
					activeLoops['game'] = False
					GD['escPressed'] = True
				elif not keys[pygame.K_ESCAPE]:
					GD['escPressed'] = False
				GD['paddleY'] = updatePaddlePosition(GD['paddleHeight'])
				GD['paddleMesh'] = rectMesh((GD['paddleX'], GD['paddleY']), GD['paddleWidth'], GD['paddleHeight'])
				pygame.draw.rect(gameDisplay, colors.white, (GD['paddleX'], GD['paddleY'], GD['paddleWidth'], GD['paddleHeight']))
				textToScreen("SCORE:" + str(GD['score']), colors.white, int(displayHeight/60), 1, 1, False, standardFont) #Score
				livesToScreen(GD['lives'])
				
				for i, ball in enumerate(GD['balls']):
					ball['cords'] = ballMovment(ball['movment'], ball['direction'], ball['cords'], timeMultipiler)
					ball['mesh'] = ballMesh(ball['cords'], ball['radius'])
					#Not using i because I have to update balls[i] and then the data refrenced to i will not be up to date
					#There are occasions where it's possible to use i.
					if rectCollision(GD['paddleMesh'], ball['mesh']): #Ball coliding with paddle?
						ball['direction'][0] = 'RIGHT'
						GD['score'] += 1
						if ball['hitted'] == False:
							GD['balls'].append(waveBall(GD['paddleHeight']))
						ball['hitted'] = True
					if rectCollision(GD['lowerWall'], ball['mesh']):
						ball['direction'][1] = 'UP'
					if ball['lost'] == False and rectCollision(GD['lostBallBorder'], ball['mesh']):
						GD['lives'] -= 1
						ball['lost'] = True
						if GD['lives'] <= 0:
							GD['gameOver'] = True
							GD['playingGame'] = False
						else:
							GD['balls'].append(waveBall(GD['paddleHeight']))
					if rectCollision(GD['upperWall'], ball['mesh']):
						ball['direction'][1] = 'DOWN'
					if ball['cords'][0] > displayWidth + ball['radius'] and ball['hitted'] == True or ball['cords'][0] + ball['radius'] < 0:
						GD['balls'].pop(i) #Removes the ball that just flew away or was missed
						ball['poped'] = True
					pygame.draw.circle(gameDisplay, ball['color'], (int(ball['cords'][0]), int(ball['cords'][1])), ball['radius'])
					if ball['poped'] == False: GD['balls'][i] = ball			
		if activeLoops['pause'] and noRender == False:
			if keys[pygame.K_ESCAPE] and GD['escPressed'] == False or continueButton.updateButton([int(displayWidth/2), int(displayHeight/2)], True): # Om inte escape var nedtryckt sisst men är nedtryckt nu
				noRender = True
				activeLoops['pause'] = False
				activeLoops['game'] = True
				GD['escPressed'] = True
				GD['pausedAt'] = frameTime
			elif not keys[pygame.K_ESCAPE]:
				GD['escPressed'] = False
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