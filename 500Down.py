#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Version:
# - 0.1
#
# Copyright 2012 Gianguido Sorà This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is
# distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the General Public License for more details. You should have received a copy of the GNU General Public License along
# with this program. If not, see http://www.gnu.org/licenses/.
#
#

import mechanize
from bs4 import BeautifulSoup
import sys

def getImage(imageURL, downloadFlag):
	# Mechanize browser istance
	browser = mechanize.Browser()

	# Browser options
	browser.set_handle_equiv(True)
	browser.set_handle_redirect(True)
	browser.set_handle_referer(True)
	browser.set_handle_robots(False)

	# refresh tweak
	browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	# set the user agent
	browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0')]

	# Open the 500px image page
	image = browser.open(imageURL)
	
	# Get the HTML
	html = image.read()
	
	# Soup-ify it
	soup =  BeautifulSoup(html)

	# Search for the tag containing the actual photo, then get the link as a variable
	for link in soup.find_all("img", class_="the_photo"):
		actualImageURL = link.get('src')
	
	# See if the download bool flag is checked, then download the image locally
	# else, display only the URL
	if downloadFlag == True:
		browser.retrieve(actualImageURL, "image.jpg")
		print("Image saved locally in the current folder")		
	else:
		print("Here's your direct link to the image --> %s") % actualImageURL
	

# A little help function
def getHelp():
	if (len(sys.argv)<2) or (sys.argv[1] == "-h") or (sys.argv[1] == "--help"):
		print("500Down: a 500px image downloader written in Python")
		print("")
		print("USAGE: %s [URL] -d") % (__file__)
		print("	-d		download the image")
		exit()

def main():
	# get help!
	getHelp()
	
	# always assume that the download flag is False
	downFlag = False
	
	# if -d is supplied as the second argument, set the download flag True
	try:
		if sys.argv[2] == "-d":
			downFlag = True
	except IndexError:
		pass
		
	# the actual function
	getImage(sys.argv[1], downFlag)
	
	exit()

if __name__ == "__main__":
	main()

