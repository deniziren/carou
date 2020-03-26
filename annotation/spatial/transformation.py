##########################################################################
# Copyright 2020 Deniz Iren. All Rights Reserved.

__name__ = 'annotation.spatial.transformation'
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


# Transform [{"x":56,"y":223},{"x":596,"y":451}] into [(56,223), (596,451)]
def dictCoordsToTupleList(aList):
    listOfTuples = []
    for point in aList:
        listOfTuples.append((point['x'], point['y']))
    return listOfTuples
	
def listCoordsToTupleList(aList):
    listOfTuples = []
    for point in aList:
        listOfTuples.append((point[0], point[1]))
    return listOfTuples