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
	lyric_text = lyricHTML.get_text()
	non_lyric_list = ["verse", "pre-chorus", "chorus", "bridge", "g-dragon", "t.o.p", "taeyang", "daesung", "seungri",
					  "chrous", "prechrous"]
	result_dict = {}
	for word in lyric_text.split():
		en_word = re.sub(r'[^\w]', '', word.lower())
		if en_word.isalpha() and en_word not in non_lyric_list:
			if en_word[0] in string.ascii_letters:
				if en_word not in result_dict:
					result_dict[en_word] = 0
				result_dict[en_word] = result_dict[en_word] + 1
	return result_dict
