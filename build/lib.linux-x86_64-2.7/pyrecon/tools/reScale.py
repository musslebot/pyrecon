#!/usr/bin/python
import argparse
parser = argparse.ArgumentParser(description='Rescales a <series> to a new <magnitude>')
parser.add_argument('series', nargs=1, type=str, help='Path to the series/sections that needs to be re-scaled')
parser.add_argument('magnitude', nargs=1, help='New magnitude to be scaled to')
parser.add_argument('outpath', nargs=1, type=str, help='Path to where the re-scaled series/sections will be placed')
args = vars(parser.parse_args())
# Assign argparse things to their variables
series = str(args['series'][0])
magnitude = float(args['magnitude'][0])
outpath = str(args['outpath'][0])

if outpath[len(outpath)-1] != '/':
    outpath += '/'
    
import pyrecon.tools.mergeTool as rmt
from pyrecon.tools.classes import *
   
def reScale(ser, newMag, outpath):
    ser = loadSeries(ser)
    ser.zeroIdentity() # Non-image contour transform -> unity transform
    
    for section in ser.sections:# Set mag field and rescale
        # img objects exist in two locations per section:
        # (1/2): Set newMag for section.imgs[0-x].mag
        oldMag = section.imgs[0].mag
        section.imgs[0].mag = float(newMag)
        scale = newMag/oldMag
        tformdImgT = scaleImgTForms(section.imgs[0].transform, scale)
        section.imgs[0].transform = tformdImgT
        for contour in section.contours:
            # (2/2): Set newMag for contour.img.mag
            if contour.img != None: # if contour is an image contour...
                contour.img = section.imgs[0] #copy section.imgs[0] to contour.img
                contour.transform = section.imgs[0].transform # copy transform
            else: # if not an image contour...
            #...rescale all the points
                pts = contour.points
                newpts = []
                for pt in pts:
                    newpts.append( (pt[0]*scale, pt[1]*scale) )
                contour.points = newpts
    # Write out series/sections
    ser.writeseries(outpath)
    ser.writesections(outpath)

def scaleImgTForms(oldT, scale):
    newT = Transform()
    newT.dim = oldT.dim
    
    newxCoefs = []
    newyCoefs = []
    if oldT.dim in range(4,7): #Poly. transform
        for newCoefs, oldCoefs in [(newxCoefs, oldT.xcoef), (newyCoefs, oldT.ycoef)]:
            newCoefs.append( oldCoefs[0]*(scale) )
            newCoefs.append( oldCoefs[1] )
            newCoefs.append( oldCoefs[2] )
            newCoefs.append( oldCoefs[3]/scale )
            newCoefs.append( oldCoefs[4]/scale )
            newCoefs.append( oldCoefs[5]/scale )
        newT.xcoef = newxCoefs
        newT.ycoef = newyCoefs
    
    else: # Affine transform
        for newCoefs, oldCoefs in [(newxCoefs, oldT.xcoef), (newyCoefs, oldT.ycoef)]:
            newCoefs.append( oldCoefs[0]*(scale) )
            newCoefs.append( oldCoefs[1] )
            newCoefs.append( oldCoefs[2] )
            newCoefs.append( oldCoefs[3] )
            newCoefs.append( oldCoefs[4] )
            newCoefs.append( oldCoefs[5] )
        newT.xcoef = newxCoefs
        newT.ycoef = newyCoefs
    
    newT.poptform()
    return newT

reScale(series, magnitude, outpath)
