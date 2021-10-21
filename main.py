import csv
from pprint import pprint
from pyzipcode import ZipCodeDatabase
from BrickseekScraper import BrickseekScraper

if __name__ == '__main__':
	zcdb = ZipCodeDatabase()

	Stores = ["Walmart", "Lowes", "Home-Depot"]
	while True:
		try:
			StoreNo = int(input("Select Store:\r\n\t" + "\r\n\t".join([store+" ["+str(index+1)+"]"  for index, store in enumerate(Stores)]) + "\r\nEnter selection #: "))
			store = Stores[StoreNo-1]
			break
		except:
			print("Invalid option! Please enter a number from list above.\r\n\r\n")

	sku = input("Enter SKU: ")
	input_zip = input("Enter source zip code: ")
	input_radius = input("Enter radius from entered zip code (in miles): ")
	sleep_duration = int(input("Enter rate limiting factor (seconds to wait after each request): "))

	#Use the ZipCodeDatabase to generate a list of zip codes within the requested radius of a source zip code.
	in_radius = [z.zip for z in zcdb.get_zipcodes_around_radius(input_zip, input_radius)]
	zipcodes = in_radius

	result = BrickseekScraper.GetBrickseekInventory(store, sku, zipcodes, sleep_duration)
	print("\r\nResults:\r\n")
	pprint(result)

	# Save results as csv
	keys = result[0].keys()
	with open(store + '-' + sku + '.csv', 'w', newline='') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(result)
	print('Done. File ' + store + "-" + sku + '.csv saved.')