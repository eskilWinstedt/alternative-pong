import pygame
import math
import time
import random
import os

pygame.init()

#Global variables:
clock = pygame.time.Clock()
standardFont = 'resources/Walkway_SemiBold.ttf'
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
				self.save()
		else:
			self.detect()
		self.updateDisplayDimensions() #Updates the displayHeight/displayWidth variables. This was ment to be removed :( but I forgot it 
		self.updateDisplay() #Sets fullscreen or not and resolution
	def save(self):
		file = open('resources/saved_settings.txt', 'w+')
		deleteFileContent(file)
		file.write(str(self.settings))
		file.close()
	def loadSettings(self):
		if checkFileExisting('resources/saved_settings.txt'):
			file = open('resources/saved_settings.txt', 'r')
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
	def __init__(self, colors, dim, text):
		'''Takes a list of different colors, a list of width and height in pixels and one optional if the button is active'''	
		#[color, hoverColor, pressedColor ,inactiveColor, textColor]
		#   0       1              2             3           4
		allButtons.append(self)
		self.colors = colors
		self.width = dim[0]
		self.height = dim[1]
		self.currentColor = 0
		self.noRender = False
		self.text = list(text)
		self.lastLoopPressing = False
		self.charsPerSecond = 3
		self.textWidth = pygame.font.SysFont(text[2], text[1]).size(text[0])[0]
		if self.textWidth > (self.width - 2): #2 = 1 px per side
			print(self.text[0] + ' button text is too wide :(')
		self.firstRender = 0
	def updateButton(self, pos, centerd, active = True, pressedBefore = False):
		if centerd == True:
			pos[0] -= int(self.width/2)
			pos[1] -= int(self.height/2)
		if active == True: #If the button is inactive, it WILL still be rendered by default but NOT collision detected
			buttonPressed = False
			cursPos = pygame.mouse.get_pos()
			cursPress = pygame.mouse.get_pressed()
			if simpleRectCollision([pos[0], pos[1], self.width, self.height], [cursPos[0], cursPos[1], 1, 1]):
				self.currentColor = 1 #Hovercolor set
				if self.lastLoopPressing == True and cursPress[0] == False:  # Button pressed on mousebutton release
					buttonPressed = True
			else:
				self.currentColor = 0 #Default color (not hovering)
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
		if active == True:
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
def simpleRectCollision(rect1, rect2):
	#common calculated values, to save CPU power
	rect1_x2 = rect1[0] + rect1[2] #the r1 x cord + width
	rect1_y2 = rect1[1] + rect1[3] #the r1 y cord + height
	rect2_x2 = rect2[0] + rect2[2] #the r2 x cord + width
	rect2_y2 = rect2[1] + rect2[3] #the r2 y cord + height
	if rect1[0] <= rect2[0] <= rect1_x2 or rect1[0] <= rect2_x2 <= rect1_x2 or rect2[0] <= rect1[0] and rect1_x2 <= rect2_x2:
		if rect1[1] <= rect2[1] <= rect1_y2 or rect1[1] <= rect2_y2 <= rect1_y2 or rect2[1] <= rect1[1] and rect1_y2 <= rect2_y2:
			return True
def rectCollision(rect1, rect2):
	# Rect elements should be (x, y, width, height)
	#Should return False if there's no collision
	XCollision = ''
	YCollision = ''
	if rect1[0] < rect2[0] <= rect1[0] + rect1[2]: #right
		if rect1[0] + rect1[2] <= rect2[0] + rect2[2]:
			XCollision = 'RIGHT'
		else: #Both inside
			XCollision = 'MIDDLE'
	elif rect2[0] <= rect1[0] < rect2[0] + rect2[2] < rect1[0] + rect1[2]:  #left
		XCollision = 'LEFT'
	elif rect2[0] <= rect1[0] and rect1[0] + rect1[2] <= rect2[0] + rect2[2]:
		XCollision = 'MIDDLE'
	if XCollision:
		if rect1[1] < rect2[1] < rect1[1] + rect1[3]:
			if rect1[1] + rect1[3] <= rect2[1] + rect2[3]:
				YCollision = 'BELOW'
			else: #Both inside
				YCollision = 'MIDDLE'
		elif rect2[1] <= rect1[1] < rect2[1] + rect2[3] < rect1[1] + rect1[3]:
			YCollision = 'OVER'
		elif rect2[1] <= rect1[1] and rect1[1] + rect1[3] <= rect2[1] + rect2[3]:
			YCollision = 'MIDDLE'
	#TRANSLATION:
	if XCollision and YCollision:
		if XCollision == 'RIGHT' and YCollision == 'BELOW':
			way = 'LOWERRIGHT'
		elif XCollision == 'RIGHT' and YCollision == 'MIDDLE':
			way = 'RIGHT'
		elif XCollision == 'RIGHT' and YCollision == 'OVER':
			way = 'UPPERRIGHT'
		elif XCollision == 'MIDDLE' and YCollision == 'BELOW':
			way = 'BELOW'
		elif XCollision == 'MIDDLE' and YCollision == 'MIDDLE':
			way = 'CENTER'
		elif XCollision == 'MIDDLE' and YCollision == 'OVER':
			way = 'OVER'
		elif XCollision == 'LEFT' and YCollision == 'BELOW':
			way = 'LOWERLEFT'
		elif XCollision == 'LEFT' and YCollision == 'MIDDLE':
			way = 'LEFT'
		elif XCollision == 'LEFT' and YCollision == 'OVER':
			way = 'UPPERLEFT'
	else:
		way = ""
	return way
def rectMesh(cord, width, height):
	x = cord[0]
	y = cord[1]
	return [x, y, width, height]
def ballMesh(cord, radius):
	x = cord[0] - radius
	y = cord[1] - radius
	diam = radius * 2
	return [x, y, diam, diam]
def cornerCollision(cords):
	#A bounce to a 45 degrees thing
	return [cords[1], cords[0]]
def updateTimeMultipiler(preClock):
	return frameTime - preClock, frameTime
def textObject(text, color, size = 25, font = standardFont):
	font = pygame.font.Font(font, size)
	textSurface = font.render(text, True, color)
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
	dict = {
	'button_width': 651,
	'button_height': 463,
	'button_font_size_y': 231,
	'startButton_pos_x': 5000,
	'startButton_pos_y': 5000,
	'optionsButton_pos_x': 5000,
	'optionsButton_pos_y': 5651,
	'exitButton_pos_x': 5000,
	'exitButton_pos_y': 6302,
	'defendButton_pos_x': 5000,
	'defendButton_pos_y': 5000,
	'continueButton_pos_x': 5000,
	'continueButton_pos_y': 5000,
	'restartButton_pos_x': 5000,
	'restartButton_pos_y': 5000,
	'quitButton_pos_x': 5000,
	'quitButton_pos_y': 6302,
	'iesButton_pos_x': 4349,
	'iesButton_pos_y': 5000,
	'noButton_pos_x': 5651,
	'noButton_pos_y': 5000,
	'menuButton_pos_x': 5000,
	'menuButton_pos_y': 5651,
	'backButton_pos_x': 5000,
	'backButton_pos_y': 5651,
	'title_text_height': 1700,
	'title_pos_x': 5000,
	'title_pos_y': 2500,
	'gamemodes_text_height': 680,
	'paused_text_height': 850,
	'paused_pos_x': 5000,
	'paused_pos_y': 2500,
	'gameover_text_height': 850,
	'gameover_pos_x': 5000,
	'gameover_pos_y': 2500,
	'realliEksit_text_height': 230,
	'realliEksit_pos_x': 5000,
	'realliEksit_pos_y': 3333,
	'hud_text_height': 167,
	'score_pos_x': 6,
	'score_pos_y': 6,
	'lives_radius_y': 83,
	'lives_spacing_x': 125,
	'paddle_width': 100,
	'paddle_height': 1000,
	'paddle_x_spacing': 300,
	'defendball_min_radius': 125,
	'defendball_max_radius': 333,
	'defendball_max_x_speed': -14000,
	'defendball_min_x_speed': -7000,
	'defendball_max_y_speed': 0,
	'defendball_min_x_spawn': 10000,
	'defendball_max_x_spawn': 20000,
	'defendball_min_y_spawn': 333,
	'defendball_max_y_spawn': 9666,
	'HUD_height': 200}
	parts = 10000
	for key, value in list(dict.items()):
		if 'height' in key.lower() or 'y' in key.lower():
			axis = displayHeight
		elif 'width' in key.lower() or 'x' in key.lower():
			axis = displayWidth
		fraction = value/parts #how much of parts?
		dict[key] = math.ceil(fraction * axis)  #Transforms the fraction of parts value to fraction of displayWidth/displayHeight. Converted to int because there is only whole pixels
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
def drawHUD():
	#Drawing a darkgrey HUD background
	pygame.draw.rect(gameDisplay, colors.der_Grey, (0, 0, displayWidth, dim['HUD_height']))
	livesToScreen() #Draws lives to screen 
	textToScreen("SCORE:" + str(GD['score']), colors.white, dim['hud_text_height'], 1, int(dim['HUD_height']/2), (False, True), standardFont)
	textToScreen("DEFEND", colors.white, dim['hud_text_height'], int(displayWidth/2), int(dim['HUD_height']/2), (True, True), standardFont)
def createOverlay(alpha):
	overlay = pygame.Surface((displayWidth, displayHeight))
	overlay = overlay.convert()
	overlay.fill((0, 0, 0))
	overlay.set_alpha(alpha)
	return overlay, overlay.get_rect() #returning surface and surface rect
def ballMovment(speed, prevCordinate, multiplier):
	return [prevCordinate[0] + speed[0] * multiplier, prevCordinate[1] + speed[1] * multiplier] #First element equals x and second y
def createBall(cords, radius, movment, color = [0,0,0]):
	return {'cords': cords, 'hitted': False, 'lost': False, 'radius': radius, 'movment': movment, 'mesh': False, 'color': color, 'poped': False, 'spawned': False, 'colManagedPaddle': False, 'colManagedUpperWall': False, 'colManagedLowerWall': False}
def randomGrey(min, max):
	g = random.randint(min ,max)
	return[g,g,g]
def defendBall():
	radius = int(random.randint(dim['defendball_min_radius'],  dim['defendball_max_radius']))
	x = random.randint(dim['defendball_min_x_spawn'], dim['defendball_max_x_spawn'])
	y = random.randint(radius + dim['HUD_height'], displayHeight - radius)
	movment = []
	movment.append(random.randint(dim['defendball_max_x_speed'], dim['defendball_min_x_speed']))
	movment.append(random.randint(numberInvert(dim['defendball_max_y_speed']), dim['defendball_max_y_speed']))
	color = randomGrey(100, 255)
	return createBall([x, y], radius, movment, color)
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
	#Misc:
	global dim
	dim = loadDesign()
	overlay, overlayRect = createOverlay(235) #Used to draw attention from the wrong buttons.
	gameIntroButtonsActive = True
	pauseButtonsActive = True
	gameOverButtonsActive = True
	loopExit = False
	preClock = time.clock() #Used to change the movment depending on the FPS
	activeLoops = {'gameIntro': True, 'pause': False, 'game': False, 'FPSMeter': False, 'modesScreen': False, 'pause': False, 'reallyExitPopup': False, 'gameOver': False}
	background = colors.black
	buttonFontSize = dim['button_font_size_y']
	buttonColorScheme = (colors.white,colors.grey,colors.der_Grey,colors.white, colors.black)
	buttonDim = [dim['button_width'], dim['button_height']]
	#Button declarations 
	startButton = Button(buttonColorScheme, buttonDim, ('START', buttonFontSize, standardFont))
	optionsButton = Button(buttonColorScheme, buttonDim, ('OPTIONS', buttonFontSize, standardFont))
	exitButton = Button(buttonColorScheme, buttonDim, ('EXIT', buttonFontSize, standardFont))
	continueButton = Button(buttonColorScheme, buttonDim, ('CONTINUE', buttonFontSize, standardFont))
	backButton = Button(buttonColorScheme, buttonDim, ('BACK', buttonFontSize, standardFont))
	menuButton = Button(buttonColorScheme, buttonDim, ('MENU', buttonFontSize, standardFont))
	quitButton = Button(buttonColorScheme, buttonDim, ('QUIT', buttonFontSize, standardFont))
	restartButton = Button(buttonColorScheme, buttonDim, ('RESTART', buttonFontSize, standardFont))
	yesButton = Button(buttonColorScheme, buttonDim, ('YES', buttonFontSize, standardFont))
	noButton = Button(buttonColorScheme, buttonDim, ('NO', buttonFontSize, standardFont))
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
			if startButton.updateButton([dim['startButton_pos_x'], dim['startButton_pos_y']], True, gameIntroButtonsActive):
				activeLoops['gameIntro'] = False
				activeLoops['modesScreen'] = True
				defendButton = Button(buttonColorScheme, buttonDim, ('DEFEND', buttonFontSize, standardFont))
				noRender = True
			if optionsButton.updateButton([dim['optionsButton_pos_x'], dim['optionsButton_pos_y']], True, gameIntroButtonsActive):
				pass
			if exitButton.updateButton([dim['exitButton_pos_x'], dim['exitButton_pos_y']], True, gameIntroButtonsActive):
				activeLoops['reallyExitPopup'] = True
				gameIntroButtonsActive = False
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
			GD['oldPaddleY'] = GD['paddleY']
			GD['paddleY'] = updatePaddlePosition(GD['paddleHeight']) #Change from GD to dim values and remove from GD when possible and secure.
			GD['paddleSpeed'] = (GD['paddleY'] - GD['oldPaddleY'])/timeMultipiler
			GD['paddleMesh'] = rectMesh((GD['paddleX'], GD['paddleY']), GD['paddleWidth'], GD['paddleHeight'])  #As above    -  ||  -
			pygame.draw.rect(gameDisplay, colors.white, (GD['paddleX'], GD['paddleY'], GD['paddleWidth'], GD['paddleHeight']))  #As above    -  ||  -
			drawHUD()
			for i, ball in enumerate(GD['balls']):
				ball['cords'] = ballMovment(ball['movment'], ball['cords'], timeMultipiler)
				ball['mesh'] = ballMesh(ball['cords'], ball['radius'])
				collisionWay = rectCollision(GD['paddleMesh'], ball['mesh'])
				if collisionWay: #Paddle and ball collision?
					if ball['colManagedPaddle'] == False:
						ball['colManagedPaddle'] = True
						if ball['hitted'] == False and not collisionWay == 'LEFT' or 'UPPERLEFT' or 'LOWERRIGHT' or 'CENTER':
							ball['hitted'] = True
							GD['score'] += 1
						if collisionWay == 'RIGHT' or collisionWay == 'LOWERRIGHT' or collisionWay == 'UPPERRIGHT':
							if ball['movment'][0] < 0:
								ball['movment'][0] = numberInvert(ball['movment'][0])
						elif collisionWay == 'OVER':
							if ball['movment'][1] >= 0:
								ball['movment'][1] = numberInvert(ball['movment'][1])
						elif collisionWay == 'BELOW':
							if ball['movment'][1] <= 0:
								ball['movment'][1] = numberInvert(ball['movment'][1])
						ball['movment'][1] += GD['paddleSpeed']/2
				else:
					ball['colManagedPaddle'] = False
				if ball['hitted'] and ball['mesh'][0] > GD['paddleMesh'][0] + GD['paddleWidth'] and ball['spawned'] == False: #Ball spawner after last ball bounced
					#Spawn new ball if the ball is hitted and to the right of the paddle (not colliding)
					GD['balls'].append(defendBall())
					ball['spawned'] = True
				if simpleRectCollision(GD['lowerWall'], ball['mesh']): #Lower wall
					if ball['colManagedLowerWall'] == False:
						ball['colManagedLowerWall'] = True
						ball['movment'][1] = numberInvert(ball['movment'][1]) #Changing to the opposite direction by converting to negative cordinates
				else:
					ball['colManagedLowerWall'] = False
				if simpleRectCollision(GD['upperWall'], ball['mesh']): #Upper wall
					if ball['colManagedUpperWall'] == False:
						ball['colManagedUpperWall'] = True
						ball['movment'][1] = numberInvert(ball['movment'][1])
				else:
					ball['colManagedUpperWall'] = False				
				if ball['lost'] == False and ball['mesh'][0] + ball['mesh'][2] <= 0: #Check if ball is lost
					ball['lost'] = True
					GD['lives'] -= 1
					GD['balls'].pop(i)
					ball['poped'] = True
					if GD['lives'] <= 0:
						activeLoops['gameOver'] = True
						activeLoops['game'] = False
						activeLoops['pause'] = False #There was a bug where the pause screen was visible when gameOverScreen was True, this is the fix
						noRender = True
					else:
						GD['balls'].append(defendBall())
				if ball['mesh'][1] > displayHeight:
					ball['mesh'][1] = displayHeight - ball['mesh'][3]
				elif ball['mesh'][1] + ball['mesh'][3] < 0:
					ball['mesh'][1] = dim['HUD_height']
				if displayWidth < ball['mesh'][0] and ball['hitted'] == True: #Hitted and outside screen?
					GD['balls'].pop(i) #Removes the ball that just flew away or was missed
					ball['poped'] = True
				if ball['poped'] == False:
					GD['balls'][i] = ball  #Updating evetything about the ball
					pygame.draw.circle(gameDisplay, ball['color'], (int(ball['cords'][0]), int(ball['cords'][1])), ball['radius'])
		if activeLoops['pause'] and noRender == False:
			textToScreen("PAUSED", colors.white, dim['paused_text_height'], dim['paused_pos_x'], dim['paused_pos_y'], (True, True), standardFont)
			if keys[pygame.K_ESCAPE] and GD['escPressed'] == False or continueButton.updateButton([dim['continueButton_pos_x'], dim['continueButton_pos_y']], True, pauseButtonsActive): # Om inte escape var nedtryckt sisst men är nedtryckt nu
				noRender = True
				activeLoops['pause'] = False
				activeLoops['game'] = True
				GD['escPressed'] = True
				GD['pausedAt'] = frameTime
			elif not keys[pygame.K_ESCAPE]:
				GD['escPressed'] = False
			#CONTINUE HERE
			if menuButton.updateButton([dim['menuButton_pos_x'], dim['menuButton_pos_y']], True, pauseButtonsActive):
				activeLoops['gameIntro'] = True
				activeLoops['pause'] = False
			if quitButton.updateButton([dim['quitButton_pos_x'], dim['quitButton_pos_y']], True, pauseButtonsActive):
				activeLoops['reallyExitPopup'] = True
				pauseButtonsActive = False #Makes the buttons on the gameOver screen unusable 
		if activeLoops['gameOver']:
			textToScreen("GAME OVER", colors.white, dim['gameover_text_height'], dim['gameover_pos_x'], dim['gameover_pos_y'], (True, True), standardFont)
			if restartButton.updateButton([dim['restartButton_pos_x'], dim['restartButton_pos_y']], True, gameOverButtonsActive):
				GD = createGameData()
				activeLoops['game'] = True
				activeLoops['gameOver'] = False
			if menuButton.updateButton([dim['menuButton_pos_x'], dim['menuButton_pos_y']], True, gameOverButtonsActive):
				activeLoops['gameIntro'] = True
				activeLoops['gameOver'] = False
			if quitButton.updateButton([dim['quitButton_pos_x'], dim['quitButton_pos_y']], True, gameOverButtonsActive):
				activeLoops['reallyExitPopup'] = True
				gameOverButtonsActive = False #Makes the buttons on the gameOver screen unusable 
		if activeLoops['reallyExitPopup']:
			gameDisplay.blit(overlay, overlayRect)  #Making a overlay over the not active game over screen
			textToScreen("DO YOU REALLY WANT TO EXIT?", colors.white, dim['realliEksit_text_height'], dim['realliEksit_pos_x'], dim['realliEksit_pos_y'], (True, True), standardFont)
			if yesButton.updateButton([dim['iesButton_pos_x'], dim['iesButton_pos_y']], True):
				pygame.quit()
				quit()
			if noButton.updateButton([dim['noButton_pos_x'], dim['noButton_pos_y']], True):
				gameOverButtonsActive = True #Now you can press the game over buttons again
				gameIntroButtonsActive = True
				pauseButtonsActive = True
				activeLoops['reallyExitPopup'] = False
		if activeLoops['FPSMeter']: #FPS loop
			print('FPS: ' + str(clock.get_fps()))
		pygame.display.update() #Updates VSync times per second
		pygame.event.clear()
		#Misc:
		if settings.settings['VSyncStatus'] == True:
			clock.tick(settings.settings['VSync']) #Used as a V-Sync feature
		if activeLoops['game'] == True:
			pygame.mouse.set_visible(False)
		else: 
			pygame.mouse.set_visible(True)
setWindowProperties()
mainLoop()