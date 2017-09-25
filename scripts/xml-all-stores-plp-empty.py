from sys import argv
import requests
import time
import os
import logging
import urllib


def get_xml_sitemap_file(file_name):
	urllib.urlretrieve("https://sssports.com/pub/sitemap/" + file_name, file_name)

def get_request_response(url):
	session = requests.Session()
	response = session.get(url, timeout=30, allow_redirects=False)	
	session.close()
	return response

def get_site_urls_list(file_path):
	input = open(file_path, 'r')
	data = input.readlines()
	temp_urls = [url.replace('<url><loc>', '') for url in data if url.count('<loc>')]
	urls = []
	for temp_url in temp_urls:
		temp_list = temp_url.split('</loc>')
		for temp_item in temp_list:
			if temp_item.count('https://') and len(temp_item) < 200:
				urls.append(temp_item)

	return urls


if __name__ == '__main__':
	
	start = 0
	end = 550
	
	main_urls_failed_dict = {}
	main_urls_not_tested_dict = {}
	main_urls_empty_dict = {}

	if not os.path.exists('logs'):
		os.mkdir('logs')
	log_path = os.path.abspath('logs')

	for language in ['en', 'ar']:
		
		for store in ['ae', 'sa', 'kw', 'qa']:
			#if store=='ae' and language=='en':continue
			server = 'sitemap_%s_%s.xml' % (store, language)
			file_path = os.path.abspath(server)
			if not os.path.isfile(file_path): 
				get_xml_sitemap_file(file_name=server)
		
			urls = get_site_urls_list(file_path)
			counter = len(urls)

			log_file = os.path.join(log_path, server + '-' + str(time.time()) + '.log')
			logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename=log_file, level=logging.DEBUG)
			logging.info('PLP health check on store [%s] sitemap' %server)
			logging.info('Found [%d] page in [%s]' %(counter, server))
			
			main_urls_failed_dict[server] = []
			main_urls_not_tested_dict[server] = []
			main_urls_empty_dict[server] = []
			
			succeed = 0
			page_count = 0

			for url in urls[start:end]:
				page_count +=1
				try:
					response = get_request_response(url)
					
					if response.ok:
						logging.info('Page [%d/%d][%s] check is [SUCCEED]' % (page_count, end, url))
						succeed +=1
						if "We can't find products" in response.text:
							logging.error('Empty category in url [%s]' % url)
							main_urls_empty_dict[server].append(url)
					else:
						logging.error('Page [%d/%d][%s] check is [FAILED]' %(page_count, end, url))
						main_urls_failed_dict[server].append(url)
				except:
						logging.warning('Page [%d/%d][%s] check is [NOT TESTED]' %(page_count, end, url))
						main_urls_not_tested_dict[server].append(url)	
				
				logging.info('Pages count [%d] and [%d] are SUCCEED and [%d] are FAILED and [%d] are NOT TESTED and [%d] are EMPTY' %(page_count, succeed, len(main_urls_failed_dict[server]), len(main_urls_not_tested_dict[server]), len(main_urls_empty_dict[server])))

			if main_urls_not_tested_dict[server]:logging.warning('Not Tested [%d] URLs:%s' %(not_tested, str(main_urls_not_tested_dict[server])))
			if main_urls_failed_dict[server]:logging.error('Failed [%d] URLs:%s' %(failed, str(main_urls_failed_dict[server])))
			if main_urls_empty_dict[server]: logging.error('Empty Categories [%d] in URLs %s' % (len(main_urls_empty_dict[server]), str(main_urls_empty_dict[server])))