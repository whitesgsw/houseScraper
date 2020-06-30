import requests
import os
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

def get_soup(url, pagination=""):
	'''Returns the soup for a given url, pagination default to None'''
	url_ = url + pagination
	req = requests.get(url_)
	soup =  BeautifulSoup(req.content, 'html.parser')
	return soup

def get_page_links(soup):
	'''Returns a list of links for properties on the page'''
	page_links = [re.findall(r'href="(.*)/"', str(block))[0] for block in soup.find_all('h2',
				{'class':'pull-left'}) if re.findall(r'href="(.*)/"', str(block)) != []]
	return page_links

def get_page_count(soup):
	'''Returns a tuple with the number of results found and the number of pages'''
	num_results = int(re.findall(r'1-20 of [0-9]+', soup.text)[0].split(" ")[-1])
	num_pages = int(num_results/20) + 1
	return (num_results, num_pages)

def make_dirs(categories):
	'''Creates files from a list to put scaping results if not exists'''
	for file in categories:
		if file not in os.listdir():
			os.mkdir("./" + file)

def save_data_to_txt(target_file, property_id, data):
	'''Creates a text file and copys data from scrape'''
	data_dict = {property_id:data}
	with open(f'{os.getcwd()}+"/"+{target_file}+"/"+{property_id}+".txt"', "w+") as file:
		file.write(data_dict)

def get_page_data_with_chromedriver(chromedriver_fpath, url):
	'''initiates a chromedriver instance and expands data and passes back to
	beautifulSoup'''
	driver = webdriver.Chrome(chromedriver_fpath)
	driver.get(url)
	view_more = driver.find_element_by_id("div-pd-suburb-more-toggle")
	view_more.click()
	page_source = driver.page_source
	data = BeautifulSoup(page_source, 'html.parser')
	return data

def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()