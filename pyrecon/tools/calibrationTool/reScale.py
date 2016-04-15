#!/usr/bin/python
"""Module for re-scaling a Series."""
import argparse

from pyrecon.classes import Transform
from pyrecon.main import openSeries
from pyrecon.tools import reconstruct_writer


def main(ser, new_mag, outpath):
    if isinstance(ser, str):
        ser = openSeries(ser)
    elif ser.__class__.__name__ == "Series":
        pass
    else:
        print("Invalid <ser> argument... try again")
        return

    # Non-image contour transform -> unity transform
    ser.zeroIdentity()
    for section in ser.sections:# Set mag field and rescale
        # img objects exist in two locations per section:
        # (1/2): Set new_mag for section.images[-1].mag
        old_mag = section.images[-1].mag
        section.images[-1].mag = float(new_mag)
        scale = new_mag / old_mag
        tformed_img_t = scaleImgTForms(
            section.images[-1].contour.transform, scale)
        section.images[-1].contour.transform = tformed_img_t
        for contour in section.contours:
            # (2/2): Set new_mag for contour.img.mag
            if contour.image is not None:
                # if contour is an Image contour
                contour.image = section.images[-1]  # copy section.images[-1] to contour.image
                contour.transform = section.images[-1].transform  # copy transform
            else:
                # if not an Image contour rescale all the points
                pts = contour.points
                newpts = []
                for pt in pts:  # TODO: this should be replaced with np.array computation
                    newpts.append((pt[0] * scale, pt[1] * scale))
                contour.points = newpts
    # Write out series/sections
    reconstruct_writer.writeSeries(ser, outpath, sections=True)


def scaleImgTForms(olt_t, scale):
    new_t = Transform()
    new_t.dim = olt_t.dim

    new_x_coefs = []
    new_y_coefs = []
    if olt_t.dim in range(4, 7):
        # Polynomial transform
        for new_coefs, old_coefs in [(new_x_coefs, olt_t.xcoef), (new_y_coefs, olt_t.ycoef)]:
            new_coefs.append(old_coefs[0] * (scale))
            new_coefs.append(old_coefs[1])
            new_coefs.append(old_coefs[2])
            new_coefs.append(old_coefs[3] / scale)
            new_coefs.append(old_coefs[4] / scale)
            new_coefs.append(old_coefs[5] / scale)
        new_t.xcoef = new_x_coefs
        new_t.ycoef = new_y_coefs

    else:
        # Affine transform
        for new_coefs, old_coefs in [(new_x_coefs, olt_t.xcoef), (new_y_coefs, olt_t.ycoef)]:
            new_coefs.append(old_coefs[0] * (scale))
            new_coefs.append(old_coefs[1])
            new_coefs.append(old_coefs[2])
            new_coefs.append(old_coefs[3])
            new_coefs.append(old_coefs[4])
            new_coefs.append(old_coefs[5])
        new_t.xcoef = new_x_coefs
        new_t.ycoef = new_y_coefs

    new_t.tform()
    return new_t

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rescales a <series> to a new <magnitude>")
    parser.add_argument("series", nargs=1, type=str,
        help="Path to the series/sections that needs to be re-scaled")
    parser.add_argument("magnitude", nargs=1,
        help="New magnitude to be scaled to")
    parser.add_argument("outpath", nargs=1, type=str,
        help="Path to where the re-scaled series/sections will be placed")
    args = vars(parser.parse_args())
    # Assign argparse things to their variables
    series = str(args["series"][0])
    magnitude = float(args["magnitude"][0])
    outpath = str(args["outpath"][0])

    if outpath[len(outpath)-1] != "/":
        outpath += "/"
    main(series, magnitude, outpath)
