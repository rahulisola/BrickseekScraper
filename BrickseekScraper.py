import json
import requests
from lxml import html
from lxml.html.clean import clean_html
import time
import re

class BrickseekScraper:
	@staticmethod
	def __Walmart(sku, zip):
		FinalStoresList = []
		url = 'https://brickseek.com/walmart-inventory-checker/'
		payload = {'method': 'sku', 'sku': sku, 'zip': zip, 'sort': 'price'}
		header_info = {
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
			'Content-type': 'application/x-www-form-urlencoded'
			}
		r = requests.post(url, data=payload, headers = header_info)    # Make a POST request with data
	
		tree = html.fromstring(clean_html(r.content))    # Parse response from the page with lxml.html

		stores =  tree.find_class('table__row')    # Get all stores from the page

		for store in stores:    # In the loop get and save in the dictionary all desired info
			item = dict()
			try:
				item['Store-name'] = ''.join(store.find_class('inventory-checker-table__store')[0].find_class('table__cell-content')[0].find_class('address-location-name')[0].text_content()).replace('\n', '').strip()
				raw_address = ''.join(store.find_class('inventory-checker-table__store')[0].find_class('table__cell-content')[0].find_class('address')[0].text_content()).strip('\n')
				item['Store-address'] = raw_address.split(' \n(')[0]
				item['Quantity'] = ''.join(store.find_class('table__cell inventory-checker-table__availability')[0].find_class('table__cell-content')[0].find_class('availability-status-indicator')[0].find_class('availability-status-indicator__text')[0].text_content())
				item['Price'] = ''.join(store.find_class('table__cell inventory-checker-table__price')[0].find_class('table__cell-content')[0].find_class('table__cell-price')[0].find_class('price-formatted')[0].text_content())
				item['ZipCode'] = item['Store-address'].split(' \n(')[0].split()[-1]
				item['Distance'] = re.findall(r"[\d.]+ Miles", raw_address)[0].replace(' Miles', '')
				FinalStoresList.append(item)
			except IndexError:
				pass
		return FinalStoresList

	@staticmethod
	def __HomeDepot(sku, zip):
		FinalStoresList = []
		url = 'https://brickseek.com/home-depot-inventory-checker/'
		payload = {'method': 'sku', 'sku': sku, 'zip': zip, 'sort': 'price'}
		header_info = {
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
			'Content-type': 'application/x-www-form-urlencoded'
			}
		r = requests.post(url, data=payload, headers = header_info)    # Make a POST request with data
	
		tree = html.fromstring(clean_html(r.content))    # Parse response from the page with lxml.html

		stores =  tree.find_class('table__row')    # Get all stores from the page

		for store in stores:    # In the loop get and save in the dictionary all desired info
			item = dict()
			try:
				item['Store-name'] = ''.join(store.find_class('inventory-checker-table__store')[0].find_class('table__cell-content')[0].find_class('address-location-name')[0].text_content()).replace('\n', '').strip()
				raw_address = ''.join(store.find_class('inventory-checker-table__store')[0].find_class('table__cell-content')[0].find_class('address')[0].text_content()).strip('\n')
				item['Store-address'] = raw_address.split(' \n(')[0]
				item['Quantity'] = ''.join(store.find_class('table__cell inventory-checker-table__availability')[0].find_class('table__cell-content')[0].find_class('availability-status-indicator')[0].find_class('availability-status-indicator__text')[0].text_content())
				item['Price'] = ''.join(store.find_class('table__cell inventory-checker-table__price')[0].find_class('table__cell-content')[0].find_class('table__cell-price')[0].text_content()).strip()
				item['ZipCode'] = item['Store-address'].split(' \n(')[0].split()[-1]
				item['Distance'] = re.findall(r"[\d.]+ Miles", raw_address)[0].replace(' Miles', '')
				FinalStoresList.append(item)
			except IndexError:
				pass
		return FinalStoresList
		
	@staticmethod
	def __Lowes(sku, zip):
		FinalStoresList = []
		url = 'https://brickseek.com/lowes-inventory-checker/'
		payload = {'method': 'sku', 'sku': sku, 'zip': zip, 'sort': 'price'}
		header_info = {
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
			'Content-type': 'application/x-www-form-urlencoded'
			}
		r = requests.post(url, data=payload, headers = header_info)    # Make a POST request with data
	
		tree = html.fromstring(clean_html(r.content))    # Parse response from the page with lxml.html

		stores =  tree.find_class('table__row')    # Get all stores from the page

		for store in stores:    # In the loop get and save in the dictionary all desired info
			item = dict()
			try:
				item['Store-name'] = ''.join(store.find_class('inventory-checker-table__store')[0].find_class('table__cell-content')[0].find_class('address-location-name')[0].text_content()).replace('\n', '').strip()
				raw_address = ''.join(store.find_class('inventory-checker-table__store')[0].find_class('table__cell-content')[0].find_class('address')[0].text_content()).strip('\n')
				item['Store-address'] = raw_address.split(' \n(')[0]
				item['Quantity'] = ''.join(store.find_class('table__cell inventory-checker-table__availability')[0].find_class('table__cell-content')[0].find_class('availability-status-indicator')[0].find_class('availability-status-indicator__text')[0].text_content())
				item['Price'] = ''.join(store.find_class('table__cell inventory-checker-table__price')[0].find_class('table__cell-content')[0].find_class('table__cell-price')[0].text_content()).strip()
				item['ZipCode'] = item['Store-address'].split(' \n(')[0].split()[-1]
				item['Distance'] = re.findall(r"[\d.]+ Miles", raw_address)[0].replace(' Miles', '')
				FinalStoresList.append(item)
			except IndexError:
				pass
		return FinalStoresList

	@staticmethod
	def GetBrickseekInventory(StoreName, sku, zipcodes, sleep_duration):
		FinalList = []
		storeList = []
		# Once a zip is processed, remove it from the list. This repeated removal is required because brickseek has it's own search radius that it uses.
		# The following few lines will remove those zip code entries that were not initially requested explicitly by the script but still returned by Brickseek as part of the results.
		# Note - this only removes it if the distance of the returned zip in the results is less than 5mi of the requested zip.
		# This is to ensure that larger (in area) zip codes with multiple stores are not ignored if a store is far away.
		# All this is done to reduce the number of wasted calls that'll be done to Brickseek for stores that have already been retrieved within results of another zip code.
		while zipcodes:
			print('Processing...')
			zip = zipcodes.pop(0) # Once a zip is processed, remove it from the list

			if StoreName == 'Walmart':
				StoreList = BrickseekScraper.__Walmart(sku, zip)
			elif StoreName == 'HomeDepot':
				StoreList = BrickseekScraper.__HomeDepot(sku, zip)
			elif StoreName == 'Lowes':
				StoreList = BrickseekScraper.__Lowes(sku, zip)

			for store in StoreList:
				# Check the distance of the store from the requested zip. If < 5mi, remove the zip from the list.
				# Once processed, then we need to remove (pop) distance attribute from the dictionary, since it is relative to each request and is useless for the final results.
				# Removing it also helps us remove duplicates and return unique list of stores and inventory results.
				if(float(store.pop('Distance', 0.0))<5.0 and store['ZipCode'] in zipcodes):
					zipcodes.remove(store['ZipCode'])
			FinalList.extend(StoreList)
			time.sleep(sleep_duration)
	
		new_l = [dict(t) for t in {tuple(d.items()) for d in FinalList}]
		return new_l