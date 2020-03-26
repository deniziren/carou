##########################################################################
# Copyright 2020 Deniz Iren. All Rights Reserved.

__name__ = 'annotation.spatial.calculation'
__author__ = 'Deniz Iren (deniziren@gmail.com)'
__version__ = '0.001'
__lastupdate__ = '10.11.2019'

def version():
	return __version__
	
def lastUpdate():
	return __lastupdate__

def name():
	return __name__


def packageInfo():
	return 'Package name: ' + __name__ + ' | ' + 'Version: ' + __version__ + ' | ' + 'Author: ' + __author__
	
##########################################################################

# Get the Euclidean distance between two points. 
# Input: PointA, PointB. 
# Points are defined as a list of two numbers that represent X and Y coordinates.  
# Returns the distance 
def EuclideanDistance2D(pointA, pointB):
    import math
    return math.sqrt((pointA[0] - pointB[0]) * (pointA[0] - pointB[0]) + (pointA[1] - pointB[1]) * (pointA[1] - pointB[1]))
	
# Get the middle of two points. 
# Input: PointA, PointB. 
# Points are defined as a list of two numbers that represent X and Y coordinates. 
# Returns a point that is in the middle of the two input points. 
def EuclideanMidPoint(pointA, pointB):
    return ((pointA[0] + pointB[0])/2 , (pointA[1] + pointB[1])/2)

# Get the centroid of a list of points
# Input: pList (a list of points) 
# Points are defined as a list of two numbers that represent X and Y coordinates.
# Returns a point that represents the centroid of the point list.
def EuclideanCentroid(pList):
    import math
    x=0
    y=0
    for i in pList:
        x = x + i[0]
        y = y + i[1]
    x = x / len(pList)
    y = y / len(pList)
    return (math.ceil(x), math.ceil(y))

# Get the shortest distance between any two points 
# Input: pList (a list of points) 
# Points are defined as a list of two numbers that represent X and Y coordinates.
# Returns the numeric value of the shortest distance between any of the points.
def getShortestDistance(pList):
    shortestDistance = 99999999
    for i in pList:
        for j in pList: 
            dist = EuclideanDistance2D(i,j)
            if i != j and dist < shortestDistance:
                shortestDistance = dist     
    return shortestDistance
	


def calculateDoubleAgreement(dictAnnotations, threshold):
    for dictKey in dictAnnotations: # Iterate over the annotations (file by file)
        # check if the key exists. If it does, take the copy of the annotations of one particular annotator into a list. 
        if 'A' in dictAnnotations[dictKey]: 
            list_A = dictAnnotations[dictKey]['A']
        else:
            list_A = []
        if 'B' in dictAnnotations[dictKey]: 
            list_B = dictAnnotations[dictKey]['B']
        else:
            list_B = []
        if 'C' in dictAnnotations[dictKey]: 
            list_C = dictAnnotations[dictKey]['C']
        else:
            list_C = []

        # Create a list that will contain the agreed points. 
        agreedPointList = [] 

        # Run pairwise distance calculations. Add the point pairs into agreedPointList that are closer to each other than the threshold. 
        for j in list_A:
            for t in list_B: 
                if EuclideanDistance2D(j, t) <= threshold:
                    agreedPointList.append(j)
                    agreedPointList.append(t)
            for t in list_C: 
                if EuclideanDistance2D(j, t) <= threshold:
                    agreedPointList.append(j)
                    agreedPointList.append(t)
        for j in list_B:
            for t in list_C: 
                if EuclideanDistance2D(j, t) <= threshold:
                    agreedPointList.append(j)
                    agreedPointList.append(t)


        finalList = []

        # Iterate over the agreedPointList. Find the duplicate points and remove them. 
        # At the end, calculate the centroid of the agreed points. 
        for i in agreedPointList:
            closeProximity = []
            closeProximity.append(i)
            for j in agreedPointList: 
                if EuclideanDistance2D(j, i) <= threshold and i!=j:
                    closeProximity.append(j)
            finalList.append(EuclideanCentroid(closeProximity))

        finalList = list( dict.fromkeys(finalList) )
        #print(finalList)

        # Do the previous step over again to get rid of further duplicates. 
        agreedPointList = finalList
        finalList = []
        for i in agreedPointList:
            closeProximity = []
            closeProximity.append(i)
            for j in agreedPointList: 
                if EuclideanDistance2D(j, i) <= threshold and i!=j:
                    closeProximity.append(j)
            finalList.append(EuclideanCentroid(closeProximity))

        finalList = list( dict.fromkeys(finalList) )
        #print(finalList)
        dictAnnotations[dictKey]['doubleAgreement'] = finalList
    return dictAnnotations
	
	
def calculateTripleAgreement(dictAnnotations, threshold):
    for dictKey in dictAnnotations: # Iterate over the annotations (file by file)
        # check if the key exists. If it does, take the copy of the annotations of one particular annotator into a list. 
        if 'A' in dictAnnotations[dictKey]: 
            list_A = dictAnnotations[dictKey]['A']
        else:
            list_A = []
        if 'B' in dictAnnotations[dictKey]: 
            list_B = dictAnnotations[dictKey]['B']
        else:
            list_B = []
        if 'C' in dictAnnotations[dictKey]: 
            list_C = dictAnnotations[dictKey]['C']
        else:
            list_C = []

        # Create a list that will contain the agreed points. 
        tripleAgreedPointList = [] 

        # Run a pairwise comparison between points in all annotators' submissions
        for j in list_A:
            for t in list_B: 
                for y in list_C: 
                    if EuclideanDistance2D(j, t) <= threshold and EuclideanDistance2D(j, y) <= threshold and EuclideanDistance2D(y, t) <= threshold:
                        agreedCentroid = EuclideanCentroid([j, t, y])
                        if agreedCentroid not in tripleAgreedPointList:
                            tripleAgreedPointList.append(agreedCentroid)

        #print(agreedPointList)

        tripleAgreedPointList = list( dict.fromkeys(tripleAgreedPointList))


        dictAnnotations[dictKey]['tripleAgreement'] = tripleAgreedPointList
    return dictAnnotations
	
def extractAgreedPointLists(dictAnnotations):
    listOfAnnotationCounts = []
    listOfDoubleAgreedPoints = []
    listOfTripleAgreedPoints = []
    for dictKey in dictAnnotations:
        if 'A' in dictAnnotations[dictKey]: 
            list_A = dictAnnotations[dictKey]['A']
        else:
            list_A = []
        if 'B' in dictAnnotations[dictKey]: 
            list_B = dictAnnotations[dictKey]['B']
        else:
            list_B = []
        if 'C' in dictAnnotations[dictKey]: 
            list_C = dictAnnotations[dictKey]['C']
        else:
            list_C = []
        if 'doubleAgreement' in dictAnnotations[dictKey]: 
            list_double = dictAnnotations[dictKey]['doubleAgreement']
            for i in list_double:
                listOfDoubleAgreedPoints.append([dictKey,i[0],i[1]])
        else:
            list_double = []
        if 'tripleAgreement' in dictAnnotations[dictKey]: 
            list_triple = dictAnnotations[dictKey]['tripleAgreement']
            for i in list_triple:
                listOfTripleAgreedPoints.append([dictKey,i[0],i[1]])
        else:
            list_triple = []
        listOfAnnotationCounts.append([dictKey, len(list_A), len(list_B), len(list_C), len(list_double), len(list_triple)])
    return listOfDoubleAgreedPoints, listOfTripleAgreedPoints, listOfAnnotationCounts

	
# Take the dataframe of annotations as input. 
# Calculate how many annotations were given per file. 
# This is used to see the frequency distributions of annotations / annotator contributions 
def getNoOfAnnotationsPerFile(dfAnnotations):
    fileList = []
    dictPoiCount = {}
    pointCount = 0
    for index, row in dfAnnotations.iterrows():
        if row['url'] not in fileList:
            fileList.append(row['url'])
        POIList = eval(row['POI'])
        pointCount = pointCount + len(POIList)
        if len(POIList) not in dictPoiCount:
            dictPoiCount[len(POIList)] = 1
        else:
            x = dictPoiCount[len(POIList)]
            dictPoiCount[len(POIList)] = x+1
    return dictPoiCount, pointCount, len(fileList) 