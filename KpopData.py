from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import string
import re

def simpleGet(url):
	"""
	Attempts to get the content at 'url' by making an HTTP GET REQUEST.
	If the content-type of response is some kind of HTML/XML, return the
	text content, otherwise, return None.
	"""
	try:
		with closing(get(url, stream = True)) as resp:
			if isGoodResponse(resp): 
				return resp.content
			else:
				return None

	except RequestException as e:
		return None

def isGoodResponse(resp):
	"""
	Returns True if the response seems to be HTML, False otherwise.
	"""
	contentType = resp.headers['Content-Type'].lower()
	return (resp.status_code == 200
			and contentType is not None
			and contentType.find('html') > -1)

def findLyrics(html):
	"""
	Returns a dict of English lyrics and their frequencies
	"""
	lyricHTML = html.find('div', class_='lyrics')
	lyricText = lyricHTML.get_text()
	resultDict = {}
	for word in lyricText.split():
		enWord = re.sub(r'[^\w]', '', word.lower())
		if enWord.isalpha():
			if enWord[0] in string.ascii_letters:
				if enWord not in resultDict:
					resultDict[enWord] = 0
				resultDict[enWord] = resultDict[enWord] + 1
		# if enWord.isalpha() and enWord[0] in string.ascii_letters:
		# 		if enWord not in resultDict:
		# 			resultDict[enWord] = 0
		# 		resultDict[enWord] = resultDict[enWord] + 1
	return resultDict
