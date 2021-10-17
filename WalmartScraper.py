import json
import csv
import requests
from lxml import html
from lxml.html.clean import clean_html
import time
import re
from pyzipcode import ZipCodeDatabase

def processInput(sku, zip):
	FinalStoresList = []
	#for zip in zipcodes:
	url = 'https://brickseek.com/walmart-inventory-checker/'
	payload = {'method': 'sku', 'sku': sku, 'zip': zip, 'sort': 'price'}
	header_info = {
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
		'Content-type': 'application/x-www-form-urlencoded'
		}
	r = requests.post(url, data=payload, headers = header_info)    # Make a POST request with data
	# print("Zip Code: " + zip + ": " + str(r.status_code))
	
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
	time.sleep(5)
	return FinalStoresList
		
if __name__ == '__main__':
	FinalList = []
	print("Start")
	
	zcdb = ZipCodeDatabase()

	sku = input("Enter SKU: ")
	input_zip = input("Enter source zip code: ")
	input_radius = input("Enter radius from entered zip code (in miles): ")

	in_radius = [z.zip for z in zcdb.get_zipcodes_around_radius(input_zip, input_radius)]
	zipcodes = in_radius

	storeList = []
	while zipcodes:
		zip = zipcodes.pop(0)
		StoreList = processInput(sku, zip)
		for store in StoreList:
			if(float(store.pop('Distance', 0.0))<5.0 and store['ZipCode'] in zipcodes):
				zipcodes.remove(store['ZipCode'])
		FinalList.extend(StoreList)
	
	new_l = [dict(t) for t in {tuple(d.items()) for d in FinalList}]
	print(new_l)
	keys = new_l[0].keys()
	with open('out.csv', 'w', newline='') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(new_l)
