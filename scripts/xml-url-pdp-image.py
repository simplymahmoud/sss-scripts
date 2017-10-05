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
	urls = {}
	for temp_url in temp_urls:
		if '</priority><image:image><image:loc>' in temp_url:
			url = temp_url.split('</loc>')[0]
			image = temp_url.split('</priority><image:image><image:loc>')[1].split('</image:loc>')[0]
			urls[url] = image

	return urls


if __name__ == '__main__':
	if len(argv) < 2:
		raise AssertionError("Usage: python xml-url-pdp-image.py sitemap.xml ... ex. python xml-url-pdp-image.py sitemap_ae_en.xml")
	
	server = argv[1]
	file_path = os.path.abspath(server)

	if not os.path.isfile(file_path): 
		get_xml_sitemap_file(file_name=server)
	
	urls = get_site_urls_list(file_path)
	counter = len(urls)
	
	main_urls_failed_dict = {}
	main_urls_failed_dict[server] = []

	main_urls_not_tested_dict = {}
	main_urls_not_tested_dict[server] = []

	product_images = []

	succeed = 0
	page_count = 0
	
	if not os.path.exists('logs'):
		os.mkdir('logs')
	log_path = os.path.abspath('logs')
	log_file = os.path.join(log_path, server + '-pdp-image-' + str(time.time()) + '.log')
	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename=log_file,level=logging.DEBUG)
	logging.info('Health check on server [%s] sitemap' %server)
	logging.info('Found [%d] page in [%s]' %(counter, server))
	
	for url in urls.keys():
		page_count +=1
		try:
			response = get_request_response(url)
			
			if response.ok:
				logging.info('Page [%d][%s] check is [SUCCEED]' % (page_count, url))
				succeed +=1
				if urls[url] not in response.text:
					logging.error('Product image [%s] in url [%s] is mismatch with the xml file [IMAGE MISMATCH]' % (urls[url], url))
					product_images.append(url)
			else:
				logging.error('Page [%d][%s] check is [FAILED]' %(page_count, url))
				main_urls_failed_dict[server].append(url)
		except:
				logging.warning('Page [%d][%s] check is [NOT TESTED]' %(page_count, url))
				main_urls_not_tested_dict[server].append(url)	
		
		logging.info('Count %d; %d are SUCCEED, %d are FAILED, %d are NOT TESTED, and %d are IMAGE MISMATCH' %(page_count, succeed, len(main_urls_failed_dict[server]), len(main_urls_not_tested_dict[server]), len(product_images)))

		if page_count%100 == 0:
			if main_urls_not_tested_dict[server]:logging.warning('Not Tested [%d] URLs:%s' %(len(main_urls_not_tested_dict[server]), str(main_urls_not_tested_dict[server])))
			if main_urls_failed_dict[server]:logging.error('Failed [%d] URLs:%s' %(len(main_urls_failed_dict[server]), str(main_urls_failed_dict[server])))
			if product_images: logging.error('Images mismatch with xml [%d] in URLs %s' % (len(product_images), str(product_images)))				

	if main_urls_not_tested_dict[server]:logging.warning('Not Tested [%d] URLs:%s' %(len(main_urls_not_tested_dict[server]), str(main_urls_not_tested_dict[server])))
	if main_urls_failed_dict[server]:logging.error('Failed [%d] URLs:%s' %(len(main_urls_failed_dict[server]), str(main_urls_failed_dict[server])))
	if product_images: logging.error('Images mismatch with xml [%d] in URLs %s' % (len(product_images), str(product_images)))