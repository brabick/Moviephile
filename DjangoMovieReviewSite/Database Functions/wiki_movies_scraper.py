import re

import bs4
import selenium
from selenium.webdriver.chrome import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WikiScraper:
	def __init__(self):
		return

	def selenium(self):
		# creates selenium to be used in making requests
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		self.browser = webdriver.Chrome(options=chrome_options)

	def wiki_request_main(self):
		# makes initial request to the movies wiki
		self.selenium()
		catagory_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J-K",
						 "L", "M", "N-O", "P", "Q-R", "S", "T", "U-V-W", "X-Y-Z"]
		self.browser.get("https://en.m.wikipedia.org/wiki/List_of_films:_numbers")
		soup = bs4.BeautifulSoup(self.browser.page_source, 'html.parser')
		self.result = soup.select('div > ul > li')

		for a in self.result[:12]:
			print(a.find('a', href=True)['href'])
			link = "https://en.m.wikipedia.org/" + a.find('a', href=True)['href']
			#self.browser.get(link)
			#print(self.browser.page_source)

	def parse_result_page(self, page_source):
		self.selenium()
		self.cast = []
		self.browser.get("https://en.m.wikipedia.org/wiki/Zero_Tolerance_(1995_film))")
		soup = bs4.BeautifulSoup(self.browser.page_source, 'html.parser')
		self.result2 = soup.find_all('li', id_=None, class_=None)
		print(self.result2[0])
		for result in self.result2:
			for res in result.find_all('b'):
				res.decompose()
			for res in result.find_all('i'):
				res.decompose()
			for res in result.find_all('span'):
				res.decompose()
			for res in result.find_all('cite'):
				res.decompose()
			for res in result.find_all('link'):
				res.decompose()
			for res in result.find_all('h2'):
				res.decompose()
			for res in result.find_all('a', class_='external text'):
				res.decompose()
			for res in result.find_all('a', class_='extiw'):
				res.decompose()
			for res in result.find_all('li', id_='footer-places-desktop-toggle'):
				res.decompose()
			for res in result.find_all('li', id_='footer-places-terms-use'):
				res.decompose()
			for res in result.find_all('a', href_='/wiki/Internet_Archive'):
				res.decompose()

		self.result2 = self.result2[:-10]

		section = soup.find_all('div', class_="div-col columns column-width")
#		print(section[0])


		"""for a in self.result2:
			print(a.text)
			self.cast.append(a.text)"""


	def add_to_db(self, result, movie_id):
		return





if __name__ == "__main__":
	e = WikiScraper()
	w = e.parse_result_page(e)
