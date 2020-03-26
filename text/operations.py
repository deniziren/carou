##########################################################################
# Copyright 2020 Deniz Iren. All Rights Reserved.

__name__ = 'text.operations'
__author__ = 'Deniz Iren (deniziren@gmail.com)'
__version__ = '0.002'
__lastupdate__ = '18.02.2020'

def version():
	return __version__
	
def lastUpdate():
	return __lastupdate__

def name():
	return __name__

def packageInfo():
	return 'Package name: ' + __name__ + ' | ' + 'Version: ' + __version__ + ' | ' + 'Author: ' + __author__
	
##########################################################################




def getName():
	return name