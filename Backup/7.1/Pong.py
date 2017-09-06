import pygame
import os.path
import math
import time
import random

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
			return False
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
		self.white = [255,255,255]
		self.grey = [128,128,128]
		self.black = [0,0,0]
		self.red = [255,0,0]
		self.green = [0,255,0]
		self.blue = [0,0,255]
		self.d_red = [150,0,0]
		self.d_green = [0,200,0]
		self.d_blue = [0,0,200]
		self.d_Grey = [64,64,64]
		self.der_Grey = [32,32,32]
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
		self.text = list(text)
		self.lastLoopPressing = False
		self.charsPerSecond = 3
		self.textWidth = pygame.font.SysFont(text[2], text[1]).size(text[0])[0]
		if self.textWidth > (self.width - 2): #2 = 1 px per side
			self.moving = True
		self.firstRender = 0
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
		if self.noRender == False: #Don't render? USEFUL when you want to make anything to a button
			if pressedBefore == True:  #Like when a link is purple, you have already pressed it. 
				self.currentColor = 2   #Pressed before color
			self.render(pos)   
		return buttonPressed #Returns if key == pressed
	def render(self, pos):
		if self.firstRender == 0:
			self.firstRender = frameTime
		pygame.draw.rect(gameDisplay, self.colors[self.currentColor], (pos[0], pos[1], self.width, self.height))	   #    c2x1  <  c1x1   <    c2x2 or c1
		textToScreen(self.text[0], self.colors[4], self.text[1], pos[0] + self.width/2, pos[1] + self.height/2, (True, True), self.text[2])
def updateAllButtonDims(dim):
	for button in allButtons:
		button.width = dim['button_width']
		button.height = dim['button_height']
		button.text[1] = dim['button_font_size_y']
def numberInvert(value):
	'''Inverts numbers to the sam value but negative/positive'''
	return value * -1
def rectCollision(rect1, rect2):
	# rect1/2 syntax = ((x, x2),(y1, y2))
	if rect2[0][0] <= rect1[0][0] <= rect2[0][1] or rect2[0][0] <= rect1[0][1] <= rect2[0][1] or rect1[0][0] <= rect2[0][0] <= rect1[0][1] or rect1[0][0] <= rect2[0][1] <= rect1[0][1]: #x1
		if rect2[1][0] <= rect1[1][0] <= rect2[1][1] or rect2[1][0] <= rect1[1][1] <= rect2[1][1] or rect1[1][0] <= rect2[1][0] <= rect1[1][1] or rect1[1][0] <= rect2[1][1] <= rect1[1][1]:
			return True
	else:
		return False
def updateTimeMultipiler(preClock):
	return frameTime - preClock, frameTime
def textObject(text, color, size = 25, font = standardFont):
	textSurface = pygame.font.SysFont(font, size).render(text, True, color)
	return textSurface, textSurface.get_rect()
def textToScreen(text, color, size, xCord, yCord, center, font):
	textSurf, textRect = textObject(text, color, size, font)
	if center[0] == True and center[1] == False:
		textRect.centerx = xCord
	elif center[1] == True and center[0] == False:
		textRect.centery = yCord
	elif center[0] and center[1]:
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
		dict[key] = math.ceil(fraction * axle)  #Transforms the fraction of parts value to fraction of displayWidth/displayHeight. Converted to int because there is only whole pixels
	return dict
def livesToScreen():
	radius = dim['lives_radius_y']
	color = colors.red
	transpColor = colors.d_red #I don't know how to use alpha colors
	spacing = dim['lives_spacing_x']
	xPos = int(displayWidth - spacing + dim['lives_radius_y']) #Change spacing if you want to change spacing
	yPos = int(dim['HUD_height']/2) #The middle of the HUD bar
	for i in range(GD['lives']):
		pygame.draw.circle(gameDisplay, transpColor, (xPos, yPos), radius)
		pygame.draw.circle(gameDisplay, color, (xPos, yPos), radius - 1)	
		xPos -= spacing
def updatePaddlePosition(paddleHeight):
	'''Makes sure that the paddle doesen't leave the screen'''
	upperLimit = dim['HUD_height']
	mouseYPos = pygame.mouse.get_pos()[1]
	if mouseYPos + paddleHeight/2 > displayHeight:
		pos = displayHeight - paddleHeight
	elif mouseYPos - paddleHeight/2 < upperLimit:
		pos = upperLimit
	else:
		pos = mouseYPos - paddleHeight/2
	return pos
def rectMesh(cord, width, height):
	x1 = cord[0]
	x2 = cord[0] + width
	y1 = cord[1]
	y2 = cord[1] + height
	return ((x1,x2),(y1,y2))
def drawHUD():
	#Drawing a darkgrey HUD background
	pygame.draw.rect(gameDisplay, colors.der_Grey, (0, 0, displayWidth, dim['HUD_height']))
	livesToScreen() #Draws lives to screen 
	textToScreen("SCORE:" + str(GD['score']), colors.white, dim['hud_text_height'], 1, int(dim['HUD_height']/2), (False, True), standardFont)
	textToScreen("DEFEND", colors.white, dim['hud_text_height'], int(displayWidth/2), int(dim['HUD_height']/2), (True, True), standardFont)
def ballMovment(speed, prevCordinate, multiplier):
	return [prevCordinate[0] + speed[0] * multiplier, prevCordinate[1] + speed[1] * multiplier] #First element equals x and second y
def createBall(cords, radius, movment, color = [0,0,0]):
	return {'cords': cords, 'hitted': False, 'lost': False, 'radius': radius, 'movment': movment, 'mesh': False, 'color': color, 'poped': False}
def randomGrey(min, max):
	g = random.randint(min ,max)
	return[g,g,g]
def defendBall():
	radius = int(random.randint(dim['defendball_min_radius'],  dim['defendball_max_radius']))
	x = random.randint(dim['defendball_min_x_spawn'], dim['defendball_max_x_spawn'])
	y = random.randint(dim['defendball_min_y_spawn'], dim['defendball_max_y_spawn'])
	movment = []
	movment.append(random.randint(dim['defendball_min_x_speed'], dim['defendball_max_x_speed']))
	movment.append(random.randint(numberInvert(dim['defendball_max_y_speed']), dim['defendball_max_y_speed']))
	color = randomGrey(100, 255)
	return createBall([x, y], radius, movment, color)
def ballMesh(cord, radius):
	x1 = cord[0] - radius
	x2 = cord[0] + radius
	y1 = cord[1] - radius
	y2 = cord[1] + radius
	return ((x1, x2),(y1, y2))
def createGameData():
	data = {
	'gamemode': 'DEFEND',
	'paddleWidth': dim['paddle_width'],
	'paddleHeight': dim['paddle_height'],
	'paddleX': dim['paddle_x_spacing'],
	'paddleY': 0,
	'upperWall': rectMesh((0, 0), displayWidth * 2, dim['HUD_height']), #Extended to ball spawn
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
	data['balls'] = [defendBall()]  #Fortsätt här...
	return data
def mainLoop():
	global dim
	dim = loadDesign()
	loopExit = False
	preClock = time.clock() #Used to change the movment depending on the FPS
	activeLoops = {'gameIntro': True, 'pause': False, 'game': False, 'FPSMeter': False, 'modesScreen': False, 'pause': False}
	background = colors.black
	buttonFontSize = dim['button_font_size_y']
	buttonColorScheme = (colors.white,colors.grey,colors.der_Grey,colors.red, colors.black)
	buttonDim = [dim['button_width'], dim['button_height']]
	#Button declarations 
	startButton = Button(buttonColorScheme, buttonDim, ('START', buttonFontSize, standardFont))
	optionsButton = Button(buttonColorScheme, buttonDim, ('OPTIONS', buttonFontSize, standardFont))
	exitButton = Button(buttonColorScheme, buttonDim, ('EXIT', buttonFontSize, standardFont))
	continueButton = Button(buttonColorScheme, buttonDim, ('CONTINUE', buttonFontSize, standardFont))
	restartButton = Button(buttonColorScheme, buttonDim, ('RESTART', buttonFontSize, standardFont))
	backButton = Button(buttonColorScheme, buttonDim, ('BACK', buttonFontSize, standardFont))
	menuButton = Button(buttonColorScheme, buttonDim, ('MENU', buttonFontSize, standardFont))
	global frameTime
	#Start of the loops:
	while  not loopExit:
		dim = loadDesign()
		updateAllButtonDims(dim)
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
			textToScreen("PONG", colors.white, dim['title_text_height'], dim['title_pos_x'], dim['title_pos_y'], (True, True), standardFont)
			if startButton.updateButton([dim['startButton_pos_x'], dim['startButton_pos_y']], True):
				activeLoops['gameIntro'] = False
				activeLoops['modesScreen'] = True
				defendButton = Button(buttonColorScheme, buttonDim, ('DEFEND', buttonFontSize, standardFont))
				noRender = True
			if optionsButton.updateButton([dim['optionsButton_pos_x'], dim['optionsButton_pos_y']], True):
				pass
			if exitButton.updateButton([dim['exitButton_pos_x'], dim['exitButton_pos_y']], True):
				pygame.quit()
				quit()
		if activeLoops['modesScreen'] and noRender == False:
			textToScreen("GAME MODES", colors.white, dim['gamemodes_text_height'], dim['title_pos_x'], dim['title_pos_y'], (True, True), standardFont)
			if defendButton.updateButton([dim['defendButton_pos_x'], dim['defendButton_pos_y']], True):
				global GD
				GD = createGameData()
				activeLoops['modesScreen'] = False
				activeLoops['game'] = True
				noRender = True
			if backButton.updateButton([dim['backButton_pos_x'], dim['backButton_pos_y']], True):
				activeLoops['modesScreen'] = False
				activeLoops['gameIntro'] = True
				noRender = True
		if activeLoops['game'] and noRender == False: #Game loop
			if not GD['playingGame'] == True:
				if GD['gameOver'] == True:
					textToScreen("GAME OVER", colors.white, dim['gameover_text_height'], dim['gameover_pos_x'], dim['gameover_pos_y'], (True, True), standardFont)
					if restartButton.updateButton([dim['restartButton_pos_x'], dim['restartButton_pos_y']], True):
						GD = createGameData()
					if menuButton.updateButton([dim['menuButton_pos_x'], dim['menuButton_pos_y']], True):
						activeLoops['gameIntro'] = True
						activeLoops['game'] = False
					#if rageQuitButton
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
				GD['paddleY'] = updatePaddlePosition(GD['paddleHeight']) #Change from GD to dim values and remove from GD when possible and secure.
				GD['paddleMesh'] = rectMesh((GD['paddleX'], GD['paddleY']), GD['paddleWidth'], GD['paddleHeight'])  #As above    -  ||  -
				pygame.draw.rect(gameDisplay, colors.white, (GD['paddleX'], GD['paddleY'], GD['paddleWidth'], GD['paddleHeight']))  #As above    -  ||  -
				for i, ball in enumerate(GD['balls']):
					ball['cords'] = ballMovment(ball['movment'], ball['cords'], timeMultipiler)
					ball['mesh'] = ballMesh(ball['cords'], ball['radius'])
					if rectCollision(GD['paddleMesh'], ball['mesh']): #Ball coliding with paddle?
						ball['movment'][0] = numberInvert(ball['movment'][0]) #Changing to the opposite direction by converting to negative cordinates
						GD['score'] += 1
						if ball['hitted'] == False:
							GD['balls'].append(defendBall())
						ball['hitted'] = True
					if rectCollision(GD['lowerWall'], ball['mesh']):
						ball['movment'][1] = numberInvert(ball['movment'][1]) #Changing to the opposite direction by converting to negative cordinates
					if ball['lost'] == False and rectCollision(GD['lostBallBorder'], ball['mesh']): #Check if ball is lost
						ball['lost'] = True
						GD['lives'] -= 1
						if GD['lives'] <= 0:
							GD['gameOver'] = True
							GD['playingGame'] = False
						else:
							GD['balls'].append(defendBall())
					if rectCollision(GD['upperWall'], ball['mesh']):
						ball['movment'][1] = numberInvert(ball['movment'][1])
					if ball['cords'][0] > displayWidth + ball['radius'] and ball['hitted'] == True or ball['cords'][0] + ball['radius'] < 0: #Hitted and outside screen?
						GD['balls'].pop(i) #Removes the ball that just flew away or was missed
						ball['poped'] = True
					pygame.draw.circle(gameDisplay, ball['color'], (int(ball['cords'][0]), int(ball['cords'][1])), ball['radius'])
					drawHUD()
					if ball['poped'] == False: GD['balls'][i] = ball  #Updating evetything about the ball
		if activeLoops['pause'] and noRender == False:
			if keys[pygame.K_ESCAPE] and GD['escPressed'] == False or continueButton.updateButton([dim['continueButton_pos_x'], dim['continueButton_pos_y']], True): # Om inte escape var nedtryckt sisst men är nedtryckt nu
				noRender = True
				activeLoops['pause'] = False
				activeLoops['game'] = True
				GD['escPressed'] = True
				GD['pausedAt'] = frameTime
			elif not keys[pygame.K_ESCAPE]:
				GD['escPressed'] = False
			textToScreen("PAUSED", colors.white, dim['paused_text_height'], dim['paused_pos_x'], dim['paused_pos_y'], (True, True), standardFont)
		if activeLoops['FPSMeter']: #FPS loop
			print('FPS: ' + str(clock.get_fps()))
		pygame.display.update() #Updates VSync times per second
		pygame.event.clear()
		if settings.settings['VSyncStatus'] == True:
			clock.tick(settings.settings['VSync']) #Used as a V-Sync feature
setWindowProperties()
mainLoop()