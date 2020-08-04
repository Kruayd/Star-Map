import regex as re
import numpy as np
import pandas as pd
import CelestiaModules.CoordinatesChangingFunctions as ccf

# Path for catalogue file
cataloguepath = 'res/catalogue/'


# Regular expressions related to Bad Barycenters (barycenters which components
# do not have data about orbits), Barycenters, stars with names like '12345 #
# starnames' and stars with names like '(12345 )"starnames"
badbarRE = re.compile('^Barycenter ?\d* ".*"\s*#')
barRE = re.compile('(?<=^Barycenter ?\d* )".*"(?=.*)')
star1RE = re.compile('(?<=^\d* # ).*')
star2RE = re.compile('(?<=^\d* ?)".*"(?=.*)')
# barRE, str1RE and star2RE are supposed to match only names and nothing else

# Regular expressions related to OrbitBarycenter variable and closed brace (})
orbitbarRE = re.compile('^\s*OrbitBarycenter.*')
closedbRE = re.compile('^}')

# Regular expressions related to right ascension, declination, distance and
# spectral type variable. They are supposed to match only ra, dec and distance
# values and the first letter of spectral type
raRE = re.compile('(?<=^\s*RA\s*)\d+(\.\d+)?')
decRE = re.compile('(?<=^\s*Dec\s*)-?\d+(\.\d+)?')
distRE = re.compile('(?<=^\s*Distance\s*)\d+(\.\d+)?')
spectypeRE = re.compile('(?<=^\s*SpectralType\s*")[a-zA-Z]')


# Dictionary that assign relative rgb values to a specific spectral class
starcolor = {'O': [66/255., 73/255., 170/255.],
             'B': [106/255., 185/255., 188/255.],
             'A': [237/255., 235/255., 237/255.],
             'F': [208/255., 187/255., 156/255.],
             'G': [251/255., 214/255., 113/255.],
             'K': [243/255., 148/255., 68/255.],
             'M': [213/255., 61/255., 50/255.],
             'R': [0/255., 255/255., 0/255.],
             'S': [0/255., 255/255., 0/255.],
             'N': [0/255., 255/255., 0/255.],
             'W': [0/255., 255/255., 0/255.],
             'L': [227/255., 12/255., 43/255.],
             'T': [113/255., 16/255., 63/255.],
             'Y': [53/255., 8/255., 43/255.],
             'C': [0/255., 255/255., 0/255.],
             'D': [214/255., 236/255., 254/255.]
            }



# Function able to parse .stc files
def stcparser(filename=str()):

    # Flag for active/open barycenter
    openbar = False
    data = []
    f = open(cataloguepath + filename, 'r')

    for line in f:
        # Find any match, in the current line, of the following regex
        badbarmatch = badbarRE.search(line)
        barmatch = barRE.search(line)
        star1match = star1RE.search(line)
        star2match = star2RE.search(line)

        # If it matches bad barycenter: skip until closed curly bracket
        if badbarmatch:
            while not closedbRE.search(line):
                line = f.readline()

        # If it matches a barycenter and there is no other active barycenter
        elif barmatch and not openbar:
            # We probably are in a new barycenter that does not orbit anything else
            # (Fundamental barycenter)
            openbar = True
            name = barmatch.group()

            # Until the closed curly bracket and until it is still true the
            # fundamental barycenter barycenter condition
            while not closedbRE.search(line) and openbar:
                # Find any match, in the current line, of the following regex
                orbitbarmatch = orbitbarRE.search(line)
                ramatch = raRE.search(line)
                decmatch = decRE.search(line)
                distmatch = distRE.search(line)

                # If "OrbitBarycenter" is found
                if orbitbarmatch:
                    # We are not in a fundamental barycenter
                    openbar = False
                # If ra, dec or distance are found, then assign them
                if ramatch:
                    ra = ramatch.group()
                if decmatch:
                    dec = decmatch.group()
                if distmatch:
                    distance = distmatch.group()

                # Read new line
                line = f.readline()

        # If it is a star and there is an active barycenter
        elif (star1match or star2match) and openbar:
            # Close the active barycenter. In this manner we make sure that only
            # the first star after a fundamental barycenter is used for
            # representing the system on the map.
            # Any possible sub-barycenter in between is skipped
            openbar = False

            # Until a closing curly bracket is found
            while not closedbRE.search(line):
                # Find any match for spectral type
                spectypematch = spectypeRE.search(line)

                # If spectral type is found, then assign it
                if spectypematch:
                    spectype = spectypematch.group()

                # Read new line
                line = f.readline()

            # Build coordinates array, change coordinates system to galactic one,
            # append rgb relative values and append to data
            coords = np.array([distance, ra, dec], dtype='single')
            star = ccf.changecoordsEQ(coords)
            star = np.append(star,starcolor[spectype]).astype('single')
            data.append(star)

        # If it is a star and there is no currently active barycenter
        elif (star1match or star2match) and not openbar:
            # Assign names
            if star1match:
                name = star1match.group()
            else:
                name = star2match.group()


            # Until a closing brace is found and it is sure that the star does not
            # orbit any barycenter
            while not closedbRE.search(line) and not openbar:
                # Find andy match
                orbitbarmatch = orbitbarRE.search(line)
                ramatch = raRE.search(line)
                decmatch = decRE.search(line)
                distmatch = distRE.search(line)
                spectypematch = spectypeRE.search(line)

                # If "OrbitBarycenter" is found
                if orbitbarmatch:
                    # The star is orbiting a barycenter
                    openbar = True
                # If ra, dec, distance and spectype are found: assign them
                if ramatch:
                    ra = ramatch.group()
                if decmatch:
                    dec = decmatch.group()
                if distmatch:
                    distance = distmatch.group()
                if spectypematch:
                    spectype = spectypematch.group()

                # Read new line
                line = f.readline()

            if not openbar:
                # Build coordinates array, change coordinates system to galactic
                # one, append rgb relative values and append to data
                coords = np.array([distance, ra, dec], dtype='single')
                star = ccf.changecoordsEQ(coords)
                star = np.append(star,starcolor[spectype]).astype('single')
                data.append(star)

            # Return openbar to false
            openbar = False

    f.close()
    return pd.DataFrame(data, columns = ['x', 'y', 'z', 'R', 'G', 'B'])
