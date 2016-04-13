"""Module for returning the calibration factor of a Series."""
import sys

import numpy as np
from skimage import transform as tf

from pyrecon.main import openSeries


if len(sys.argv) > 1:
    path_to_series = str(sys.argv[1])
    # functions initiated at bottom of page


def findCalFactor(series):
    """Return the scale factor that was applied to a Series' transformation."""
    if isinstance(series, str):
        ser = openSeries(series)
    elif series.__class__.__name__ == "Series":
        ser = series
    else:
        print("Invalid argument... try again.")
        return
    # create list of all image transforms in a series
    imgtforms = []
    for section in ser.sections:
        imgtform = section.images[-1].contour.transform
        if imgtform.isAffine():
            imgtform.tag = "Transform for "+section.images[-1].src+" in section "+section.name # Change tag to include the section it belongs to
            # Convert to Affine Transform and append
            a = imgtform.xcoef
            b = imgtform.ycoef
            tmatrix = np.array( [a[1],a[2],a[0],b[1],b[2],b[0],0,0,1] ).reshape((3,3)) # 1x9 -> 3x3
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
    min_scale = tforms2[0]._tform.scale[0] #start with 1st transform in list
    mint_t = tforms2[0]
    multi_mins = []

    for tform in tforms2[1:]:
        if abs(tform._tform.scale[0]) - 1 < abs(min_scale) - 1:
            min_scale = tform._tform.scale[0]
            mint_t = tform
            multi_mins = []

        elif abs(tform._tform.scale[0]) - 1 == abs(min_scale) - 1:
            multi_mins.append(tform)

    output = str(mint_t.tag)
    for elem in multi_mins:
        output += "\n" + elem.tag
    print "{}\nwith a scale of {}".format(output, min_scale)
    return min_scale
