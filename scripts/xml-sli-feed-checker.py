from sys import argv
import requests
import time
import os
import logging

quick_mode = True

def get_request_response(url):
	session = requests.Session()
	response = session.get(url, timeout=30, allow_redirects=False)	
	session.close()
	return response

def get_site_urls_list(file_path):
	input = open(file_path, 'r')
	lines = input.readlines()
	urls = []
	urls_dict = {}
	for line in lines:				
		if 'sku="' in line:
			urls_dict['sku'] = line.split('sku="')[1].split('">')[0]
		elif '<price>' in line:
			urls_dict['aed_price'] = line.split('<aed>')[1].split('</aed>')[0].split('.')[0].replace(',', '')
			urls_dict['sar_price'] = line.split('<sar>')[1].split('</sar>')[0].split('.')[0].replace(',', '')
			urls_dict['kwd_price'] = line.split('<kwd>')[1].split('</kwd>')[0].split('.')[0].replace(',', '')
			urls_dict['qar_price'] = line.split('<qar>')[1].split('</qar>')[0].split('.')[0].replace(',', '')
			urls_dict['usd_price'] = line.split('<usd>')[1].split('</usd>')[0].split('.')[0].replace(',', '')
			if 'aed_special_price' in line:
				urls_dict['aed_special_price'] = line.split('<aed_special_price>')[1].split('</aed_special_price>')[0].split('.')[0].replace(',', '')
			if 'sar_special_price' in line:
				urls_dict['sar_special_price'] = line.split('<sar_special_price>')[1].split('</sar_special_price>')[0].split('.')[0].replace(',', '')
			if 'kwd_special_price' in line:
				urls_dict['kwd_special_price'] = line.split('<kwd_special_price>')[1].split('</kwd_special_price>')[0].split('.')[0].replace(',', '')	
			if 'qar_special_price' in line:
				urls_dict['qar_special_price'] = line.split('<qar_special_price>')[1].split('</qar_special_price>')[0].split('.')[0].replace(',', '')	
			if 'usd_special_price' in line:
				urls_dict['usd_special_price'] = line.split('<usd_special_price>')[1].split('</usd_special_price>')[0].split('.')[0].replace(',', '')
		elif '<final_price>' in line:
			urls_dict['final_price'] = line.split('<final_price>')[1].split('</final_price>')[0].split('.')[0].replace(',', '')
		elif '<url_key><![CDATA[' in line:
			urls_dict['url'] = line.split('<url_key><![CDATA[')[1].split(']]></url_key>')[0]
		elif '<visibility>' in line:
			visibility = int(line.split('<visibility>')[1].split('</visibility>')[0])
			if visibility != 1: urls.append(urls_dict)	
			urls_dict = {}
	
	return urls

def get_price_values_from_page_response(response):
	prices = {'price': '-1', 'special_price': '-1'}
	lines = response.text.splitlines()		
	for line in lines:
		if 'itemprop="offers" itemscope itemtype="http://schema.org/Offer">' in line:
			prices['special_price'] = str(line.split('itemprop="offers"')[1].split('<span class="price"')[1].split(' ')[1].split('</span>')[0].split('.')[0].replace(',', '') )
		if '<span class="price"' in line:
			prices['price'] = str(line.split('<span class="price"')[1].split(' ')[1].split('</span>')[0].split('.')[0].replace(',', '') )

	return prices

if __name__ == '__main__':
	if len(argv) < 2:
		raise AssertionError("Usage: python xml-criteo-feed-checker.py sitemap.xml start[optional] end[optional] ... ex. python xxml-criteo-feed-checker.py criteo_feed_en_ae.xml 500 1000")
	
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
	main_urls_not_tested_dict = {}
	main_urls_price_failed_dict = {}

	succeed = 0
	page_count = 0

	if not os.path.exists('logs'):
		os.mkdir('logs')
	log_path = os.path.abspath('logs')
	log_file = os.path.join(log_path, server + '-sli-feed-' + str(time.time()) + '.log')
	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename=log_file,level=logging.DEBUG)
	logging.info('Health check on server [%s] riteo feed sitemap' %server)
	logging.info('Found [%d] page in [%s]' %(counter, server))	

	for url in urls[start:end]:
		page_count +=1
		if quick_mode:
			if server not in main_urls_not_tested_dict.keys():main_urls_not_tested_dict[server]=[]
			if server not in main_urls_price_failed_dict.keys():main_urls_price_failed_dict[server]=[]
			if server not in main_urls_failed_dict.keys():main_urls_failed_dict[server]=[]
			try:
				response = get_request_response('https://en-ae.sssports.com/' + url['url'])
				
				if response.ok:
					logging.info('Page [%d/%d][%s] check is [SUCCEED]' % ( page_count+start, counter, str(url['url']) ))
					succeed +=1
					prices = get_price_values_from_page_response(response)
					if url['final_price'] not in prices.values():
						logging.error('Page [%d/%d][%s] check is [PRICE MISMATCH]' %(page_count+start, counter, str(url['url']) ))
						logging.error('XML price is [%s] and product page price(s) are %s' %( str(url['final_price']), str(prices)))						
						main_urls_price_failed_dict[server].append('Page URL [%s] price(s) %s is not matching feeds price %s' % ( str(url['url']), str(prices), str(url['final_price']) ))

				else:
					logging.error('Page [%d/%d][%s] check is [FAILED]' %( page_count+start, counter, str(url['url']) ))					
					main_urls_failed_dict[server].append(url['url'])

			except:
					logging.warning('Page [%d/%d][%s] check is [NOT TESTED]' %( page_count+start, counter, str(url['url']) ))					
					main_urls_not_tested_dict[server].append(url['url'])	
			logging.info('Pages count [%d] and [%d] are SUCCEED and [%d] are FAILED and [%d] are NOT TESTED and [%d] are MISMATCH' %(page_count, succeed, len(main_urls_failed_dict[server]), len(main_urls_not_tested_dict[server]), len(main_urls_price_failed_dict[server])))
		else:
			language = 'en'
			for store in ['ae', 'sa', 'kw', 'qa']:
				server = 'https://%s-%s.sssports.com/' % (language, store)
				if store == 'ae':
					currency = 'aed'
				elif store == 'sa':
					currency = 'sar'
				elif store == 'kw':
					currency = 'kwd'
				elif store == 'qa':
					currency = 'qar'
				else:
					currency = 'usd'
				if server not in main_urls_price_failed_dict.keys():main_urls_price_failed_dict[server]=[]
				if server not in main_urls_failed_dict.keys():main_urls_failed_dict[server]=[]
				if server not in main_urls_not_tested_dict.keys():main_urls_not_tested_dict[server]=[]					
				try:
					response = get_request_response( server + url['url'] )
					
					if response.ok:
						logging.info('Page [%d/%d][%s] check is [SUCCEED]' % ( page_count+start, counter, str(url['url']) ))
						succeed +=1
						prices = get_price_values_from_page_response(response)
						if url['%s_price'%currency] not in prices.values():
							logging.error('Page [%d/%d][%s] check is [PRICE MISMATCH]' %(page_count+start, counter, str(url['url']) ))
							logging.error('XML price is [%s] and product page price(s) are %s' %( str(url['final_price']), str(prices)))
							main_urls_price_failed_dict[server].append('%s price(s) %s is not matching feeds price %s' % ( str(url['url']), str(prices), str(url['final_price']) ))

					else:
						logging.error('Page [%d/%d][%s] check is [FAILED]' %( page_count+start, counter, str(url['url']) ))
						main_urls_failed_dict[server].append(url['url'])

				except:
						logging.warning('Page [%d/%d][%s] check is [NOT TESTED]' %( page_count+start, counter, str(url['url']) ))
						main_urls_not_tested_dict[server].append(url['url'])					

				logging.info('Pages count [%d] and [%d] are SUCCEED and [%d] are FAILED and [%d] are NOT TESTED and [%d] are MISMATCH' %(page_count, succeed, len(main_urls_failed_dict[server]), len(main_urls_not_tested_dict[server]), len(main_urls_price_failed_dict[server])))
		
		if page_count%100 == 0:
			if main_urls_not_tested_dict.values():logging.warning('Not Tested URLs:%s' %(str(main_urls_not_tested_dict)))
			if main_urls_failed_dict.values():logging.error('Failed URLs:%s' %(str(main_urls_failed_dict)))
			if main_urls_price_failed_dict.values():logging.error('Failed prices details; %s' %( str(main_urls_price_failed_dict) ) )

	if main_urls_not_tested_dict.values():logging.warning('Not Tested URLs:%s' %(str(main_urls_not_tested_dict)))
	if main_urls_failed_dict.values():logging.error('Failed URLs:%s' %(str(main_urls_failed_dict)))
	if main_urls_price_failed_dict.values():logging.error('Failed prices details; %s' %( str(main_urls_price_failed_dict) ) )