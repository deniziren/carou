##########################################################################
# Copyright 2020 Deniz Iren. All Rights Reserved.

__name__ = 'web.search'
__author__ = 'Deniz Iren (deniziren@gmail.com)'
__version__ = '0.001'
__lastupdate__ = '14.03.2020'

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
	
import requests
from bs4 import BeautifulSoup

# Searches for a query string on Yandex and downloads the first image that is found.
def searchAndRetrieveImage(query):
    

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    #query = 'backgammon'
    query = query.replace(' ', '%20').replace('&','%26')
    html = requests.get("https://yandex.com/images/search?text=" + query, headers=headers) 

    #print(html.status_code)
    html_soup_content = BeautifulSoup(html.text, features="lxml")

    html_soup_content
    temp = html_soup_content.findAll("img", {"class":"serp-item__thumb justifier__thumb"})
    if html.status_code == requests.codes.ok:
        query_url = temp[0]['src']
        return requests_image('https:' + query_url, query)

import requests
from io import open as iopen

# Gets an image stream url (Yandex domain) and saves it to the local folder.
def requests_image(file_url, query):
   
    file_name=query.replace(' ', '').replace('%20', '_').replace('%26','_and_') +'.jpg'
    i = requests.get(file_url)
    if i.status_code == requests.codes.ok:
        #print('writing...')
        with iopen(file_name, 'wb') as file:
            file.write(i.content)
    else:
        print('err: '. i.status_code)
        return False
    return file_name
#requests_image(file_url)