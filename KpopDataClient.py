from KpopData import *
from bs4 import BeautifulSoup
from collections import OrderedDict

def fileReader(fileName):
	fileObj = open(fileName, 'r')
	links = []
	for line in fileObj:
		links.append(line)
	fileObj.close()
	return links


"""
Main Program
"""
links = fileReader('links.txt') 

fullDict = {}

for link in links:
	soup = BeautifulSoup(simpleGet(link), 'html.parser')
	songDict = findLyrics(soup)
	for word in songDict:
		if word not in fullDict:
			fullDict[word] = songDict[word]
		fullDict[word] = fullDict[word] + songDict[word]

# a dictionary in descending order by word frequency
fullDict = OrderedDict(sorted(fullDict.items(), key=lambda i: i[1], reverse=True))

for word in fullDict:
	print('{} - {}'.format(word, fullDict[word]))