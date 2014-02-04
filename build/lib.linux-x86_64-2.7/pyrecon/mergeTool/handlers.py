'''Terminal(Non-GUI) handler functions for mergeTool conflicts'''
# SECTION
# - Contours
def sectionContours(uniqueA, compOvlp, confOvlp, uniqueB):
	'''Returns list of contours to be added to merged series'''
	outputContours = []

	# Unique: Add unique contours to output
	outputContours.extend(uniqueA)
	outputContours.extend(uniqueB)

	# Completely overlapping: Add a single copy of compOvlp pair to output
	for pair in compOvlp:
  		outputContours.append(pair[0])

	# Conflicting: Handle conflicting overlaps
	for pair in confOvlp:
  		print('Conflicting contour overlap')
  		print(pair[0].__dict__) #===
 		print(pair[1].__dict__) #=== 
		sel = raw_input('Please enter 1, 2, or both to select what to output: ')
		if sel == '1':
	  		outputContours.append(pair[0])
		elif sel == '2':
			outputContours.append(pair[1])
		else:
		  	outputContours.append(pair[0])
		  	outputContours.append(pair[1])
	return outputContours

# - Image
def sectionImages(imageA, imageB):
	padding = 20
	print('Section image conflicts:')
	print('='*(padding*3))
	# Header
	print( 'Attribute'.ljust(padding) ),
	print( 'Image 1 Value'.ljust(padding) ),
	print( 'Image 2 Value'.ljust(padding) )
	print( '---------'.ljust(padding) ),
	print( '-------------'.ljust(padding) ),
	print( '-------------'.ljust(padding) )

	# Attributes
	print( 'Source:'.ljust(padding) ),
	print( imageA.src.ljust(padding) ),
	print( imageB.src.ljust(padding) )
	print( 'Magnification:'.ljust(padding) ),
	print( str(imageA.mag).ljust(padding) ),
	print( str(imageB.mag).ljust(padding) )
	print('='*(padding*3))
	resp = 0
	while resp != 1 or resp != 2:
		resp = int(input('Enter either 1 or 2 to choose image for merged section: '))
		if resp == 1:
			return imageA
		elif resp == 2:
			return imageB
	return
