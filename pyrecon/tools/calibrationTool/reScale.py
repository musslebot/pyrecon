#!/usr/bin/python
from pyrecon.main import openSeries
from pyrecon.classes import Transform
from pyrecon.tools import handleXML as xml
import argparse
 
def main(ser, newMag, outpath):
    if type(ser) == type(''):
        ser = openSeries(ser)
    elif ser.__class__.__name__ == 'Series':
        pass
    else:
        print('Invalid <ser> argument... try again')
        return

    # Non-image contour transform -> unity transform
    ser.zeroIdentity() 
    for section in ser.sections:# Set mag field and rescale
        # img objects exist in two locations per section:
        # (1/2): Set newMag for section.images[-1].mag
        oldMag = section.images[-1].mag
        section.images[-1].mag = float(newMag)
        scale = newMag/oldMag
        tformdImgT = scaleImgTForms(section.images[-1].contour.transform, scale)
        section.images[-1].contour.transform = tformdImgT
        for contour in section.contours:
            # (2/2): Set newMag for contour.img.mag
            if contour.image is not None: # if contour is an image contour...
                contour.image = section.images[-1] #copy section.images[-1] to contour.image
                contour.transform = section.images[-1].transform # copy transform
            else: # if not an image contour...
            #...rescale all the points
                pts = contour.points
                newpts = []
                for pt in pts: #=== this should be replaced with np.array computation
                    newpts.append( (pt[0]*scale, pt[1]*scale) )
                contour.points = newpts
    # Write out series/sections
    xml.writeSeries(ser, outpath, sections=True)

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
    
    newT.tform()
    return newT

if __name__ == '__main__':
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
    main(series, magnitude, outpath)
