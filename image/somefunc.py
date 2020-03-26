##########################################################################
# Copyright 2020 Deniz Iren. All Rights Reserved.

__name__ = 'image.somefunc'
__author__ = 'Deniz Iren (deniziren@gmail.com)'
__version__ = '0.001'
__lastupdate__ = '09.11.2019'

def version():
	return __version__
	
def lastUpdate():
	return __lastupdate__

def name():
	return __name__
	
def packageInfo():
	return 'Package name: ' + __name__ + ' | ' + 'Version: ' + __version__ + ' | ' + 'Author: ' + __author__
	
##########################################################################

def somefunc():
	print('Where is Set?')
	return True