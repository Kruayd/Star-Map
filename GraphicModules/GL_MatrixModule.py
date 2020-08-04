import numpy as np



# All the following code take into account that numpy is row major so, a vector
# looks like [a, b, c] and not like |a|
#                                   |b|
#                                   |c|
#
# If you are used to do matrix multiplication in column major, remember that in
# order to transition from column to row, or vice versa, you simply need to
# transpose everything:
# transpose(A*B*C*columnvector) = rowvector*t(C)*t(B)*t(A)


#  ________________________________________________
# |                                                |
# | module part relative to graphic transformation |
# |________________________________________________|
#


# Matrix for orthographic projection
def orthographic(l, r, b, t, n, f, datatype = 'single'):

    matrix = np.array([[     2 / (r-l),              0,              0, 0],
                       [             0,      2 / (t-b),              0, 0],
                       [             0,              0,     -2 / (f-n), 0],
                       [-(r+l) / (r-l), -(t+b) / (t-b), -(f+n) / (f-n), 1]],
                      dtype = datatype, order = 'F')

    return matrix

# Matrix for a perspective projection
def perspective(fov, WbH, n, f, datatype = 'single', degree = True):

    if degree:
        fov *= np.pi / 180.

    Sx = 1 / np.tan(fov / 2)
    Sy = WbH / np.tan(fov / 2)

    matrix = np.array([[Sx,  0,                0,  0],
                       [ 0, Sy,                0,  0],
                       [ 0,  0,     -f / (f - n), -1],
                       [ 0,  0, -f * n / (f - n),  0]],
                      dtype = datatype, order = 'F')

    return matrix

# Matrix for translating the view (basis transformation)
def viewtranslation(x0, y0, z0, datatype = 'single'):

    matrix = np.array([[  1,   0,   0, 0],
                       [  0,   1,   0, 0],
                       [  0,   0,   1, 0],
                       [-x0, -y0, -z0, 1]],
                      dtype = datatype, order = 'F')

    return matrix

# Matrix fot rotating the view (basis transformation)
def viewrotation(a, b, c, datatype = 'single', degree = True):

    if degree:
        a *= np.pi / 180.
        b *= np.pi / 180.
        c *= np.pi / 180.

    a *= -1
    b *= -1
    c *= -1

    xrotation = np.array([[1,          0,         0, 0],
                          [0,  np.cos(a), np.sin(a), 0],
                          [0, -np.sin(a), np.cos(a), 0],
                          [0,          0,         0, 1]],
                         dtype = datatype, order = 'F')

    yrotation = np.array([[np.cos(b), 0, -np.sin(b), 0],
                          [        0, 1,          0, 0],
                          [np.sin(b), 0,  np.cos(b), 0],
                          [        0, 0,          0, 1]],
                         dtype = datatype, order = 'F')

    zrotation = np.array([[ np.cos(c), np.sin(c), 0, 0],
                          [-np.sin(c), np.cos(c), 0, 0],
                          [         0,         0, 1, 0],
                          [         0,         0, 0, 1]],
                         dtype = datatype, order = 'F')

    matrix = matrixmultiplication(zrotation, yrotation, xrotation)

    return matrix

# Matrix fot translating models (object transformation)
def modeltranslation(x0, y0, z0, datatype = 'single'):

    matrix = np.array([[ 1,  0,  0, 0],
                       [ 0,  1,  0, 0],
                       [ 0,  0,  1, 0],
                       [x0, y0, z0, 1]],
                      dtype = datatype, order = 'F')

    return matrix

# Matrix fot rotating models (object transformation)
def modelrotation(a, b, c, datatype = 'single', degree = True):

    if degree:
        a *= np.pi / 180.
        b *= np.pi / 180.
        c *= np.pi / 180.

    xrotation = np.array([[1,          0,         0, 0],
                          [0,  np.cos(a), np.sin(a), 0],
                          [0, -np.sin(a), np.cos(a), 0],
                          [0,          0,         0, 1]],
                         dtype = datatype, order = 'F')

    yrotation = np.array([[np.cos(b), 0, -np.sin(b), 0],
                          [        0, 1,          0, 0],
                          [np.sin(b), 0,  np.cos(b), 0],
                          [        0, 0,          0, 1]],
                         dtype = datatype, order = 'F')

    zrotation = np.array([[ np.cos(c), np.sin(c), 0, 0],
                          [-np.sin(c), np.cos(c), 0, 0],
                          [         0,         0, 1, 0],
                          [         0,         0, 0, 1]],
                         dtype = datatype, order = 'F')

    matrix = matrixmultiplication(zrotation, yrotation, xrotation)

    return matrix

# Remember that a basis trasformation is the inverse of the corrseponding
# object transformation

# Recursive function to multiply everything in one passage
def matrixmultiplication(*args, datatype = 'single'):

    result = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]],
                      dtype = datatype, order = 'F')

    for matrix in args:

        result = np.matmul(result, matrix, order = 'F')

    return result
