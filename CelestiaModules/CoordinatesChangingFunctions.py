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
# | module part relative to matrix transformations |
# |________________________________________________|
#

# Matrix fot rotating coordinates around x axis
def Rx(a, datatype = 'single'):

    xrotation = np.array([[1,          0,         0],
                          [0,  np.cos(a), np.sin(a)],
                          [0, -np.sin(a), np.cos(a)]],
                         dtype = datatype)

    return xrotation

# Matrix fot rotating coordinates around y axis
def Ry(a, datatype = 'single'):

    yrotation = np.array([[np.cos(a), 0, -np.sin(a)],
                          [        0, 1,          0],
                          [np.sin(a), 0,  np.cos(a)]],
                         dtype = datatype)

    return yrotation

# Matrix fot rotating coordinates around z axis
def Rz(a, datatype = 'single'):

    zrotation = np.array([[ np.cos(a), np.sin(a), 0],
                          [-np.sin(a), np.cos(a), 0],
                          [         0,         0, 1]],
                         dtype = datatype)

    return zrotation

# Recursive function to multiply everything in one passage
def matrixmultiplication(*args, datatype = 'single'):

    result = np.array([[1, 0, 0],
                       [0, 1, 0],
                       [0, 0, 1]],
                      dtype = datatype)

    for matrix in args:

        result = np.matmul(result, matrix)

    return result

# Remember that a basis trasformation is the inverse of the corrseponding
# object transformation



#  ________________________________________________
# |                                                |
# | module part relative to matrix transformations |
# |________________________________________________|
#

# Function needed to transition from equatorial to galactic rectangular
# ones
def changecoordsEQ(coords = np.array([0, 0, 0], dtype = 'single')):

    # Data taken from https://en.wikipedia.org/wiki/Celestial_coordinate_system
    # and referring to J2000
    RAg = 192.85948     # Right ascension of the Galactic North Pole
    DECg = 27.12825     # Declination of the Galactic North Pole
    Lnp = 122.93192     # Galactic longitude of the North Celestial Pole

    # Evaluation of Euler angles in radiants
    Ac = (RAg + 90) * np.pi / 180   # Right ascension of the intersection
                                    # between the galactic and equatorial
                                    # planes

    Pc = (90 - DECg) * np.pi / 180  # Conversion of Galactic North Pole
                                    # declination to spherical polar angle

    CB = (90 - Lnp) * np.pi / 180   # Angle between the galactic and equatorial
                                    # planes intersection and the center of the
                                    # galaxy direction

    # What follows has as a precondition the fact that the coordinates are
    # ordered like this: (distance, right ascension, declination)

    # Bring everything to radiants
    coords[1] *= np.pi / 180
    coords[2] = (90 - coords[2]) * np.pi / 180

    # Getting from spherical to cartesian coordinates
    coords1 = np.array([coords[0] * np.cos(coords[1]) * np.sin(coords[2]),
                        coords[0] * np.sin(coords[1]) * np.sin(coords[2]),
                        coords[0] * np.cos(coords[2])],
                       dtype = 'single')

    # Set of rotations that brings the Vernal Point (x-axis) on the
    # intersection between the galactinc and equatorial planes (Rz(Ac)), then place the
    # North Pole (z-axis) in the direction of the Galactic North Pole (Rx(Pc)) and finally align
    # the x-axis with the Center of the Milky Way (Rz(CB))
    #
    # Since we have to transform the coordinates, and not the basis, we have to
    # use the inverse transformation:
    # [Rz(Ac) * Rx(Pc) * Rz(CB)]**-1 = [Rz(CB)**-1] * [Rx(Pc)**-1] * [Rz(Ac)**-1]
    # = Rz(-CB) * Rx(-Pc) * Rz(-Ac)
    Rz1 = Rz(-CB)
    Rx1 = Rx(-Pc)
    Rz2 = Rz(-Ac)

    return matrixmultiplication(coords1, Rz1, Rx1, Rz2)


# Function needed to transition from celestia/ecliptic to galactic rectangular
# ones
def changecoordsEC(coords = np.array([0, 0, 0], dtype = 'single')):

    # Data taken from https://en.wikipedia.org/wiki/Celestial_coordinate_system
    # and referring to J2000
    RAg = 192.85948     # Right ascension of the Galactic North Pole
    DECg = 27.12825     # Declination of the Galactic North Pole
    Lnp = 122.93192     # Galactic longitude of the North Celestial Pole

    # Evaluation of Euler angles in radiants
    Ac = (RAg + 90) * np.pi / 180   # Right ascension of the intersection
                                    # between the galactic and equatorial
                                    # planes

    Pc = (90 - DECg) * np.pi / 180  # Conversion of Galactic North Pole
                                    # declination to spherical polar angle

    CB = (90 - Lnp) * np.pi / 180   # Angle between the galactic and equatorial
                                    # planes intersection and the center of the
                                    # galaxy direction

    # The following operation are based on what's stated here:
    # https://en.wikibooks.org/wiki/Celestia/Binary_Star_File
    e = 23.4392911 * np.pi / 180

    # Rotation matrix that transforms ecliptic coordinates into equatorial
    # ones
    Rx = mm.Rx(e)

    coords1 = matrixmultiplication(coords, Rx)

    # Celestia y and z coordinates are swappend, wile x is inverted
    x1 = -coords1[0]
    y1 =  coords1[2]
    z1 =  coords1[1]

    coords1[0] = x1
    coords1[1] = y1
    coords1[2] = z1

    # Set of rotations that brings the Vernal Point (x-axis) on the
    # intersection between the galactinc and equatorial planes (Rz(Ac)), then place the
    # North Pole (z-axis) in the direction of the Galactic North Pole (Rx(Pc)) and finally align
    # the x-axis with the Center of the Milky Way (Rz(CB))
    #
    # Since we have to transform the coordinates, and not the basis, we have to
    # use the inverse transformation:
    # [Rz(Ac) * Rx(Pc) * Rz(CB)]**-1 = [Rz(CB)**-1] * [Rx(Pc)**-1] * [Rz(Ac)**-1]
    # = Rz(-CB) * Rx(-Pc) * Rz(-Ac)
    Rz1 = mm.Rz(-CB)
    Rx1 = mm.Rx(-Pc)
    Rz2 = mm.Rz(-Ac)

    return matrixmultiplication(coords1, Rz1, Rx1, Rz2)
