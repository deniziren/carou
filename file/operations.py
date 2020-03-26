##########################################################################
# Copyright 2020 Deniz Iren. All Rights Reserved.

__name__ = 'file.operations'
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

def getFileList(directoryPath, fileType = '*'):
	import os
	fileList = []
	if fileType == '*':
		for filename in os.listdir(directoryPath):
			if filename not in fileList:
				fileList.append(filename)
	return fileList

import string
def sanitizeFileName(badString):
    goodString = ''
    goodString = ''.join(filter(lambda x: x in string.printable, badString))
    goodString = goodString.translate(str.maketrans('', '', string.punctuation))
    goodString = goodString.translate(str.maketrans('', '', ' '))
    return goodString

def getName():
	return name