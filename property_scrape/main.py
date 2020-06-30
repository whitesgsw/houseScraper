import requests
import os
import re
from bs4 import BeautifulSoup
import utils
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

if __name__ == "__main__":

	url_dict = {"for_sale":"https://reiwa.com.au/for-sale/perth~region/",
			"for_rent":"https://reiwa.com.au/rental-properties/perth~region/",
			"sold":"https://reiwa.com.au/sold/perth~region/"}

	DRIVER_FPATH = "chromedriver.exe"
	BASE_URL = "https://reiwa.com.au"

	# make directory files
	utils.make_dirs(url_dict.keys())
	#debug
	print(os.listdir())

	#call progress bar
	#for item in utils.progressBar(url_dict.keys(), prefix='Category',suffix = 'Complete', length = 50):
		
	for category in url_dict.keys():
		#read in links data
		link_name_str = f'{category}+"links.txt"'

		if link_name_str in os.listdir(f'./{category}'):
			with open(f'{os.getcwd()}+"/link_name_str"', "r+") as file:
				scraped_link_list = file.readlines()
		else:
			scraped_link_list = []

		# get main page soup
		main_page_soup = utils.get_soup(url_dict[category])

		# get number of pages
		page_count = utils.get_page_count(main_page_soup)[1]

		# iterate through pages and scrape links
		links = []

		
		for page in range(1, page_count):
			
			# get links from page
			print(url_dict[category]+"?page-"+str(page))

			soup = utils.get_soup(url_dict[category], "?page-"+str(page))
			links = links + utils.get_page_links(soup)

			print(links)
		# save links to txt for later
		utils.save_data_to_txt(category, link_name_str, links)

		# get list of propertyIDs that have been parsed

		# iterate through links and generate soup
		for link in links:

			#get ID from link
			prop_id = link.split("-")[-1]

			# if id not in scraped list for category then get data
			if prop_id not in scraped_link_list:

				# get soup
				data = utils.get_page_data_with_chromedriver(DRIVER_FPATH, BASE_URL+link)

				# save data to textfile
				# link is hyphenated and last is propertyID
				utils.save_data_to_txt(category, prop_id, data)

				# add prop_id to scraped link list
				scraped_link_list.append(prop_id)

		#update scraped link list file
		with open(f'{os.getcwd()}+"/link_name_str"', "r+") as file:
			file.write(scraped_link_list)




