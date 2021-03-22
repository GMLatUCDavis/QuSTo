'''
QuSlicer ver 0.5 for QuSTO
Josh Medina
Updated 1/19/2021
'''
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Import
import csv, os
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
from scipy import interpolate
from scipy import stats
from scipy import signal
from scipy.signal import find_peaks

class QuSlicer:
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Main functions

    # slices verts along an axis according to floor, ceil
    def sliceVerts(verts, axis, floor, ceil):

        # slice direction
        #X is 0, Y is 1, Z is 3
        axis = QuSlicer.getAxis(axis)

        # n is either X, Y, or Z depending on slice direction
        slicedVerts = []
        nCoords = [item[axis] for item in verts]
        nMin, nMax = min(nCoords), max(nCoords)
        nRange = nMax - nMin
        nMin += (nRange * floor) # The bottom % of slice
        nMax -= (nRange * (1-ceil)) # The top % of slice

        # slice
        for coord in verts:
            n = coord[axis]
            if (n >= nMin and n <= nMax):
                slicedVerts.append(coord)

        # sort
        slicedVerts = sorted(slicedVerts, key=itemgetter(0))

        # scale
        slicedVerts = QuSlicer.setScale(slicedVerts)

        ''' 
        # debug - vert slice in red
        x = QuSlicer.parseCoord(slicedVerts, 0)
        z = QuSlicer.parseCoord(slicedVerts, 1)
        plt.plot(x, z, '-r')
        '''
        return np.array(slicedVerts, dtype='float32')

    # skims the bottom off sliced verts by defining new floor
    # positive skims the top, negative skims the bottom
    def skimSlice(verts, axis, skim):

        # skim axis (typically perpendicular to slice direction)
        axis = QuSlicer.getAxis(axis)
        skimmedVerts = []
        nCoords = [item[axis] for item in verts]
        nMin, nMax = min(nCoords), max(nCoords)
        nRange = nMax - nMin

        # skim direction
        pos = skim > 0

        # skim based on skimPoint (percentage)
        if (pos):
            skimPercent = nRange * abs(skim)
            skimPoint = nMax - skimPercent
        else:
            skimPercent = nRange * abs(skim)
            skimPoint = nMin + skimPercent

        # skim
        for coord in verts:
            n = coord[axis]
            if (pos):
                if (n >= skimPoint):
                    skimmedVerts.append(coord)
            else:
                if (n <= skimPoint):
                    skimmedVerts.append(coord)

        return np.array(skimmedVerts, dtype='float32')

    # smooths the sliced verts
    def smoothSlice(verts, smoothSteps, scale):

        # Average for noise. Default median window length 7
        smoothedVerts = QuSlicer.smoothAverage(verts, 7)

        # Bias towards peaks, away from troughs
        for i in range(smoothSteps):
            smoothedVerts = QuSlicer.smoothPeaks(smoothedVerts, 1, 1)
        for i in range(smoothSteps):
            smoothedVerts = QuSlicer.smoothPeaks(smoothedVerts, 1, 0)

        # Apply spline
        smoothedVerts = QuSlicer.smoothSpline(smoothedVerts, 1000, 2)

        # Resets the scale for correct Height values in QuSto
        smoothedVerts = QuSlicer.setScale(smoothedVerts, scale)

        return smoothedVerts


    # averages noise caught from overlapping vertices via cumulative sum
    # The 'thicker' the slice, the more noise there will be to average.
    # windowLength is the size of the sliding window within which to median
    def smoothAverage(verts, windowLength):

        # seperate coords
        x = QuSlicer.parseCoord(verts, 0)
        z = QuSlicer.parseCoord(verts, 1)
        '''
        # debug - plots slice vertices in red
        plt.plot(x, z, '-r')
        '''
        # calculate Median
        x = signal.medfilt(x, windowLength)
        z = signal.medfilt(z, windowLength)
        '''
        # debug - plots slice's surface vertices in blue
        plt.plot(x, z, 'o')
        plt.show()
        '''
        return(tuple(zip(x, z)))

    # Finds peaks/troughs in data according to dist and pos
    # Peaks are preserved, troughs are thrown away
    def smoothPeaks(verts, dist, pos):

        smoothedVerts = []
        x = QuSlicer.parseCoord(verts, 0)
        z = QuSlicer.parseCoord(verts, 1)

        # Positive peaks or negative peaks (troughs)
        if (pos == 0):
            # Find valleys, remove them
            listVerts = [*verts]  #tuple to list
            valleys, _ = find_peaks(np.negative(z), distance=dist)
            valleyVerts = []
            for x in range(len(verts)):
                if x in valleys:
                    valleyVerts.append(verts[x])

            valleySet = set(valleyVerts)
            l3 = [x for x in listVerts if x not in valleySet]
            smoothedVerts = l3
        else:
            # Find peaks, keep them
            peaks, _ = find_peaks(z, distance=dist)
            for i in range(len(verts)):
                if i in peaks:
                    smoothedVerts.append(verts[i])

        return smoothedVerts

    # smooths the averaged data according to spline
    # default degree is 3, or cubic. Modify to increase smoothing degree.
    def smoothSpline(verts, resolution, degree):

        verts = np.array(verts).tolist()
        unDupVerts = []
        #find a way to average duplicate x values

        # seperate coords
        x = np.array(QuSlicer.parseCoord(verts, 0))
        z = np.array(QuSlicer.parseCoord(verts, 1))

        # sorts ouut those with duplicate x
        u, c = np.unique(x, return_counts=True)
        dup = u[c > 1]

        # new x is 200 equally spaced values between the min and max of input
        # the bounds can be adjusted for outliers via buffer - careful here.
        buffer = 0
        xnew = np.linspace(x.min()+buffer, x.max()-buffer, resolution)


        # define spline in terms of xnew, zsmooth
        spl = interpolate.make_interp_spline(x, z, k=degree)
        zsmooth = spl(xnew)

        '''
        #debug - plot smoothed verts in green
        plt.plot(xnew, zsmooth, '-g')
        '''

        # put them together
        return tuple(zip(xnew, zsmooth))

# ---------------------------------------------------------------------------------------------------------------------------------------------
# Other functions

    # scales verts and sets min to 0 via offset
    def setScale(verts, setScale=None):

        verts = [list(x) for x in verts]
        x = QuSlicer.parseCoord(verts, 0)
        z = QuSlicer.parseCoord(verts, 1)
        xOffset, zOffset = 0 - min(x), 0 - min(z)

        # auto scale
        if setScale is None:

            scale = 1

            # sets scale via reciprocal according to bounds
            if abs(max(x)) < 10 or abs(max(z)) < 20: scale = 10
            if abs(max(x)) < 1 or abs(max(z)) < 2: scale = (1/abs(max(x))) * 100

            for coord in verts:

                # offsets verts so min is 0 in X and Z
                if xOffset > 0: coord[0] += xOffset
                else: coord[0] -= xOffset
                if zOffset > 0: coord[1] += zOffset
                else: coord[1] -= zOffset

                # scales verts last
                coord[0] *= scale
                coord[1] *= scale

        # input scale
        else:

            # scales verts first
            for coord in verts:
                coord[0] *= setScale
                coord[1] *= setScale

            # finds new min z for offset
            z = QuSlicer.parseCoord(verts, 1)
            zOffset = 0 - min(z)

            # offsets verts last
            for coord in verts:
                if zOffset < 0: coord[1] += zOffset
                else: coord[1] -= zOffset

        return verts

    def median(x,w):
        return(np.median(x[w:]))

    # remove all vert pairs with a Y value that's lower than average
    def removeLower(verts):

        # seperate z
        z = QuSlicer.parseCoord(verts, 1)
        # calculate y average
        yAvg = 0
        for i in range(len(z)):
            yAvg= yAvg + z[i] / len(z)

        skimmedVerts = []

        # skim
        for coord in verts:
            if (coord[1] >= yAvg):
                skimmedVerts.append(coord)
        return np.array(skimmedVerts, dtype='float32')

    # X=0, Y=1, Z=2
    def getAxis(axis):
        axisNum = 0
        if (axis == 'y'): axisNum = 1
        if (axis =='z'): axisNum = 2
        return (axisNum)

    # x,z into x and z
    def parseCoord(verts, axis):
        parsed = []
        for coord in verts:
            parsed.append(coord[axis])
        return parsed

    def writeCSV(output, path, filename):

        csvFileObj = open(os.path.join(path, filename), 'w', newline='')
        csvWriter = csv.writer(csvFileObj)
        csvWriter.writerow('XZ')
        for i in output:
            csvWriter.writerow(i)
        csvFileObj.close()

