'''Terminal(Non-GUI) handler functions for mergeTool conflicts'''

def sectionContours(uniqueA, compOvlp, confOvlp, uniqueB):
	
	return

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
