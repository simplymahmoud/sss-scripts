from sys import argv
import requests
import time
import os
import logging


def get_request_response(url):
	session = requests.Session()
	response = session.get(url, timeout=30, allow_redirects=False)	
	session.close()
	return response

def get_site_urls_list(file_path):
	input = open(file_path, 'r')
	lines = input.readlines()
	urls = []
	for line in lines:
		if '<link><![CDATA[' in line:
			product_url = line.split('<link><![CDATA[')[1].split(']]></link><description>')[0]			
		elif '<g:price>' in line:
			if '<g:sale_price>' in line:
				product_price = str(line.split('<g:sale_price>')[1].split('</g:sale_price>')[0].split('.')[0].replace(',', '') )
			else:
				product_price = str(line.split('<g:price>')[1].split('</g:price>')[0].split('.')[0].replace(',', '') )
			urls.append([product_url, product_price])
	return urls

def get_price_values_from_page_response(response):
	prices = []
	lines = response.text.splitlines()		
	for line in lines:
		if 'itemprop="offers" itemscope itemtype="http://schema.org/Offer">' in line:
			prices.append(str(line.split('itemprop="offers"')[1].split('<span class="price"')[1].split(' ')[1].split('</span>')[0].split('.')[0].replace(',', '') ))
		elif '<span class="price"' in line:#<span class="price">AED 59.00</span>
			prices.append(str(line.split('<span class="price"')[1].split(' ')[1].split('</span>')[0].split('.')[0].replace(',', '') ))
		


	if prices == []:prices = [-1]
	return prices

if __name__ == '__main__':
	if len(argv) < 2:
		raise AssertionError("Usage: python xml-google-feed-checker.py sitemap.xml start[optional] end[optional] ... ex. python xml-google-feed-checker.py google_feed_en_ae.xml 500 1000")
	
	server = argv[1]
	file_path = os.path.abspath(server)
	
	start = 0
	if len(argv) > 2:
		start = int(argv[2])

	urls = get_site_urls_list(file_path)
	counter = len(urls)
	
	end = len(urls) - 1
	if len(argv) > 3:
		end = int(argv[3])
	
	main_urls_failed_dict = {}
	main_urls_failed_dict[server] = []

	main_urls_not_tested_dict = {}
	main_urls_not_tested_dict[server] = []

	main_urls_price_failed_dict = {}
	main_urls_price_failed_dict[server] = []

	succeed = 0
	page_count = 0

	if not os.path.exists('logs'):
		os.mkdir('logs')
	log_path = os.path.abspath('logs')
	log_file = os.path.join(log_path, server + '-google-feed-' + str(time.time()) + '.log')
	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename=log_file,level=logging.DEBUG)
	logging.info('Health check on server [%s] riteo feed sitemap' %server)
	logging.info('Found [%d] page in [%s]' %(counter, server))
	
	for url in urls[start:end]:
		page_count +=1
		try:
			response = get_request_response(url[0])
			
			if response.ok:
				logging.info('Page [%d/%d][%s] check is [SUCCEED]' % ( page_count+start, counter, str(url[0]) ))
				succeed +=1
				prices = get_price_values_from_page_response(response)
				if url[1] not in prices:
					logging.error('Page [%d/%d][%s] check is [PRICE MISMATCH]' %(page_count+start, counter, str(url[0]) ))
					logging.error('XML price is [%s] and product page price(s) are %s' %( str(url[1]), str(prices)))
					main_urls_price_failed_dict[server].append('Page URL [%s] price(s) %s is not matching feeds price %s' % ( str(url[0]), str(prices), str(url[1]) ))


			else:
				logging.error('Page [%d/%d][%s] check is [FAILED]' %( page_count+start, counter, str(url[0]) ))
				main_urls_failed_dict[server].append(url[0])
		
		except:
				logging.warning('Page [%d/%d][%s] check is [NOT TESTED]' %( page_count+start, counter, str(url[0]) ))
				main_urls_not_tested_dict[server].append(url[0])	
		
		logging.info('Pages count [%d] and [%d] are SUCCEED and [%d] are FAILED and [%d] are NOT TESTED and [%d] are MISMATCH' %(page_count, succeed, len(main_urls_failed_dict[server]), len(main_urls_not_tested_dict[server]), len(main_urls_price_failed_dict[server])))

		if page_count%100 == 0:
			if main_urls_not_tested_dict[server]:logging.warning('Not Tested [%d] URLs:%s' %(len(main_urls_not_tested_dict[server]), str(main_urls_not_tested_dict[server])))
			if main_urls_failed_dict[server]:logging.error('Failed [%d] URLs:%s' %(len(main_urls_failed_dict[server]), str(main_urls_failed_dict[server])))
			if main_urls_price_failed_dict[server]:
				logging.error('Failed prices [%d] Details;' % len(main_urls_price_failed_dict[server]))
				[logging.info(line) for line in main_urls_price_failed_dict[server]]

	if main_urls_not_tested_dict[server]:logging.warning('Not Tested [%d] URLs:%s' %(len(main_urls_not_tested_dict[server]), str(main_urls_not_tested_dict[server])))
	if main_urls_failed_dict[server]:logging.error('Failed [%d] URLs:%s' %(len(main_urls_failed_dict[server]), str(main_urls_failed_dict[server])))
	if main_urls_price_failed_dict[server]:
		logging.error('Failed prices [%d] Details;' % len(main_urls_price_failed_dict[server]))
		[logging.info(line) for line in main_urls_price_failed_dict[server]]
