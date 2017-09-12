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
	if len(argv) < 2:
		raise AssertionError("Usage: python xml-url-plp-empty.py sitemap.xml start[optional] end[optional] ... ex. python xml-url-plp-empty.py sitemap_ae_en.xml 0 500")
	
	server = argv[1]
	file_path = os.path.abspath(server)

	if not os.path.isfile(file_path): 
		get_xml_sitemap_file(file_name=server)
	
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

	empty_categories = []
	coming_soon_image = []

	succeed = 0
	page_count = 0
	
	if not os.path.exists('logs'):
		os.mkdir('logs')
	log_path = os.path.abspath('logs')
	log_file = os.path.join(log_path, server + '-getter-' + str(time.time()) + '.log')
	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename=log_file,level=logging.DEBUG)
	logging.info('Health check on server [%s] sitemap' %server)
	logging.info('Found [%d] page in [%s]' %(counter, server))
	
	for url in urls[start:end]:
		page_count +=1
		try:
			response = get_request_response(url)
			
			if response.ok:
				logging.info('Category [%d/%d][%s] check is [SUCCEED]' % (page_count+start, end, url))
				succeed +=1
				if "We can't find products" in response.text:
					logging.error('Empty category in url [%s] [EMPTY]' % url)
					empty_categories.append(url)
				#elif "d_coming-soon.jpg/media/catalog/product\d" in response.text:
				else:
					text = re.compile(r"d_coming-soon.jpg/media/catalog/product\d+")
					if hasattr(response.text, 'group'):
						logging.error('Category in url [%s] has image coming-soon.jpg [COMING SOON]' % url)
						coming_soon_image.append(url)

			else:
				logging.error('Category [%d/%d][%s] check is [FAILED]' %(page_count+start, end, url))
				main_urls_failed_dict[server].append(url)
		except:
				logging.warning('Category [%d/%d][%s] check is [NOT TESTED]' %(page_count+start, end, url))
				main_urls_not_tested_dict[server].append(url)	
		
		logging.info('Count %d; %d are SUCCEED, %d are FAILED, %d are NOT TESTED, %d are EMPTY, and %d having COMING SOON image' %(page_count, succeed, len(main_urls_failed_dict[server]), len(main_urls_not_tested_dict[server]), len(empty_categories), len(coming_soon_image)))

	if main_urls_not_tested_dict[server]:logging.warning('Not Tested [%d] URLs:%s' %(len(main_urls_not_tested_dict[server]), str(main_urls_not_tested_dict[server])))
	if main_urls_failed_dict[server]:logging.error('Failed [%d] URLs:%s' %(len(main_urls_failed_dict[server]), str(main_urls_failed_dict[server])))
	if empty_categories: logging.error('Empty Categories [%d] in URLs %s' % (len(empty_categories), str(empty_categories)))
	if coming_soon_image: logging.error('Categories with coming soon image [%d] in URLs %s' % (len(coming_soon_image), str(coming_soon_image)))