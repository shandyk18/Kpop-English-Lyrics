from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from langdetect import detect
from collections import OrderedDict
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
	lyricHTML = html.find('div', class_='box-body')
	lyricText = lyricHTML.get_text()
	resultMap = {}
	for word in lyricText.split():
		#print(word)
		enWord = re.sub(r'[^\w]', '', word.lower())
		if enWord.isalpha(): 
			if enWord[0] in string.ascii_letters:
				if enWord not in resultMap:
					resultMap[enWord] = 0
				resultMap[enWord] = resultMap[enWord] + 1
	return OrderedDict(sorted(resultMap.items()))

"""
Main Program
"""
raw_html = simpleGet('https://www.lyrics.co.kr/?p=514420')
html = BeautifulSoup(raw_html, 'html.parser')
resultMap = findLyrics(html)
for word in resultMap:
	print('word: {} appearances: {}'.format(word, resultMap[word]))
