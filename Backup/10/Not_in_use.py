''' 
	rectColors = [[255,255,255],[150,150,150]]
	changeSize = Button(buttonColorScheme, buttonDim, ('size', buttonFontSize, standardFont))
	rect_mesh = rectMesh((100 ,100), 50, 50)
	mouseSize = [20, 20]
	#IN LOOP!!!:
			mouseMesh = rectMesh(pygame.mouse.get_pos(), mouseSize[0], mouseSize[1])
		pygame.draw.rect(gameDisplay, (150, 150, 150), mouseMesh)
		col = simpleRectCollision(rect_mesh, mouseMesh)
		if col:
			pygame.draw.rect(gameDisplay, rectColors[1], rect_mesh)
			print(col)
		else:
			pygame.draw.rect(gameDisplay, rectColors[0], rect_mesh)
		if changeSize.updateButton([500, 300], True):
			if mouseSize[0] == 20:
				mouseSize = [70, 70]
			elif mouseSize[0] == 70:
				mouseSize = [20, 20]