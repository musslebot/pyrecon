import sys
from pyrecon.tools.classes import *
from skimage import transform as tf
import numpy as np

if len(sys.argv) > 1:
    path_to_series = str( sys.argv[1] )

def findCalFactor(path_to_series):
    '''Returns the scale factor that was applied to the transformation of a series'''
    ser = loadSeries(path_to_series)
    # create list of all image transforms in a series
    imgtforms = []
    for section in ser.sections:
        imgtform = section.imgs[0].transform
        if imgtform.isAffine():
            imgtform.tag = 'Transform for '+section.imgs[0].name+' in section '+section.name # Change tag to include the section it belongs to
            # Convert to Affine Transform and append
            a = imgtform.xcoef
            b = imgtform.ycoef
            tmatrix = np.array( [a[1],a[2],a[0],b[1],b[2],b[0],0,0,1] ).reshape((3,3))
            imgtform._tform = tf.AffineTransform(tmatrix)
            imgtforms.append(imgtform)   
    
    # find tforms where shear and rotation = 0, scale x and scale y are the same       
    tforms2 = [] 
    for t in imgtforms:
        if int(t._tform.rotation) == 0 and \
        int(t._tform.shear) == 0 and \
        t._tform.scale[0] == t._tform.scale[1]:
            tforms2.append(t)
    
    # find tforms with scale values closest to 1
    minScale = tforms2[0]._tform.scale[0] #start with 1st transform in list
    minT = tforms2[0]
    multiMins = []
    
    for tform in tforms2[1:]:
        if abs(tform._tform.scale[0])-1 < abs(minScale)-1:
            minScale = tform._tform.scale[0]
            minT = tform
            multiMins = []
            
        elif abs(tform._tform.scale[0])-1 == abs(minScale)-1:
            multiMins.append(tform)
    
    output = str(minT.tag)
    for elem in multiMins:
        output += '\n'+elem.tag
    print( output+'\nwith a scale of '+ str(minScale) )
    return minScale

if __name__ == '__main__':
    findCalFactor(path_to_series)