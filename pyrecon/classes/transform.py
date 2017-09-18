import numpy as np
from skimage import transform as tf


def get_skimage_transform(xcoef=None, ycoef=None, dim=None):
    """ Returns a skimage.transform.
    """
    if not xcoef or not ycoef or dim is None:
        return None
    a = xcoef
    b = ycoef
    # Affine transform
    if dim in range(0, 4):
        if dim == 0:
            tmatrix = np.array(
                [1, 0, 0, 0, 1, 0, 0, 0, 1]
            ).reshape((3, 3))
        elif dim == 1:
            tmatrix = np.array(
                [1, 0, a[0], 0, 1, b[0], 0, 0, 1]
            ).reshape((3, 3))
        elif dim == 2:
            # Special case, swap b[1] and b[2]
            # look at original Reconstruct code: nform.cpp
            tmatrix = np.array(
                [a[1], 0, a[0], 0, b[1], b[0], 0, 0, 1]
            ).reshape((3, 3))
        elif dim == 3:
            tmatrix = np.array(
                [a[1], a[2], a[0], b[1], b[2], b[0], 0, 0, 1]
            ).reshape((3, 3))
        return tf.AffineTransform(tmatrix)
    # Polynomial transform
    elif dim in range(4, 7):
        tmatrix = np.array(
            [a[0], a[1], a[2], a[4], a[3], a[5], b[0], b[1], b[2], b[4], b[3], b[5]]
        ).reshape((2, 6))
        # create matrix of coefficients
        tforward = tf.PolynomialTransform(tmatrix)

        def getrevt(pts):  # pts are a np.array
            newpts = []  # list of final estimates of (x,y)
            for i in range(len(pts)):
                # (u,v) for which we want (x,y)
                u, v = pts[i, 0], pts[i, 1]  # input pts
                # initial guess of (x,y)
                x0, y0 = 0.0, 0.0
                # get forward tform of initial guess
                uv0 = tforward(np.array([x0, y0]).reshape([1, 2]))[0]
                u0 = uv0[0]
                v0 = uv0[1]
                e = 1.0  # reduce error to this limit
                epsilon = 5e-10
                i = 0
                while e > epsilon and i < 100:  # NOTE: 10 -> 100
                    i += 1
                    # compute Jacobian
                    l = a[1] + a[3] * y0 + 2.0 * a[4] * x0
                    m = a[2] + a[3] * x0 + 2.0 * a[5] * y0
                    n = b[1] + b[3] * y0 + 2.0 * b[4] * x0
                    o = b[2] + b[3] * x0 + 2.0 * b[5] * y0
                    p = l * o - m * n  # determinant for inverse
                    if abs(p) > epsilon:
                        # increment x0,y0 by inverse of Jacobian
                        x0 = x0 + ((o * (u - u0) - m * (v - v0)) / p)
                        y0 = y0 + ((l * (v - v0) - n * (u - u0)) / p)
                    else:
                        # try Jacobian transpose instead
                        x0 = x0 + (l * (u - u0) + n * (v - v0))
                        y0 = y0 + (m * (u - u0) + o * (v - v0))
                    # get forward tform of current guess
                    uv0 = tforward(np.array([x0, y0]).reshape([1, 2]))[0]
                    u0 = uv0[0]
                    v0 = uv0[1]
                    # compute closeness to goal
                    e = abs(u - u0) + abs(v - v0)
                # append final estimate of (x,y) to newpts list
                newpts.append((x0, y0))
            newpts = np.asarray(newpts)
            return newpts
        tforward.inverse = getrevt
        return tforward


class Transform(object):
    """ Class representing a RECONSTRUCT Transform.
    """

    def __init__(self, **kwargs):
        """ Assign instance attributes to provided args/kwargs.
        """
        self.dim = kwargs.get("dim")
        self.xcoef = kwargs.get("xcoef")
        self.ycoef = kwargs.get("ycoef")

    @property
    def _tform(self):
        """ Return a skimage transform object.
        """
        return get_skimage_transform(
            xcoef=self.xcoef,
            ycoef=self.ycoef,
            dim=self.dim
        )

    def __eq__(self, other):
        """ Allow use of == operator.
        """
        to_compare = ["dim", "xcoef", "ycoef"]
        for k in to_compare:
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __ne__(self, other):
        """ Allow use of != operator.
        """
        return not self.__eq__(other)

    def isAffine(self):
        """ Returns True if the transform is affine.
        """
        xcheck = self.xcoef[3:6]
        ycheck = self.ycoef[3:6]
        for elem in xcheck:
            if elem != 0:
                return False
        for elem in ycheck:
            if elem != 0:
                return False
        return True
