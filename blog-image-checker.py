from sys import argv
import requests
import time
import os
import logging


def head_request_response(url):
	session = requests.Session()
	response = session.head(url, timeout=30, allow_redirects=False)
	session.close()
	return response

def get_request_response(url):
	session = requests.Session()
	response = session.get(url, timeout=30, allow_redirects=False)	
	session.close()
	return response

def get_site_urls_list(file_path):
	input = open(file_path, 'r')
	lines = input.readlines()
	urls = [line.split('\n')[0] for line in lines]
	return urls

def get_images_urls_from_page_response(response):
	images_urls = []
	lines = response.text.splitlines()		
	for line in lines:
		if 'src="https://blog.sssports.com/wp-content/uploads/' in line:
			images_urls.append(line.split('src="')[1].split('"')[0])
		elif 'rackcdn.com' in line:
			if 'desktop-banner" style="background-image:url' in line:
				images_urls.append(line.split('desktop-banner" style="background-image:url(')[1].split(')">')[0])
			if 'mobile-banner"' in line:
				images_urls.append(line.split('mobile-banner" style="background-image:url(')[1].split(')">')[0])
			if '<img class' in line:
				images_urls.append(line.split('src="')[1].split('"')[0])

	return images_urls


if __name__ == '__main__':
	if len(argv) < 2:
		raise AssertionError("Usage: python blog-image-checker.py blog-urls.txt start[optional] end[optional] ... ex. python blog-image-checker.py blog-urls.txt 500 1000")
	
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

	failed_images_dict = {}

	succeed = 0
	failed = 0
	not_tested = 0
	page_count = 0

	if not os.path.exists('logs'):
		os.mkdir('logs')
	log_path = os.path.abspath('logs')
	log_file = os.path.join(log_path, server + '-' + str(time.time()) + '.log')
	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename=log_file,level=logging.DEBUG)
	logging.info('Health check on server [%s] sitemap' %server)
	logging.info('Found [%d] page in [%s]' %(counter, server))
	
	for url in urls[start:end]:
		page_count +=1
		try:
			response = get_request_response(url)
			if response.ok:
				logging.info('Page [%d/%d][%s] check is [SUCCEED]' % (page_count+start, counter, url))
				succeed +=1
				images_urls = get_images_urls_from_page_response(response=response)			
				logging.info('Found [%d] images in page [%s]' %(len(images_urls), url))
				for image_url in images_urls:				
					logging.info('Checking image [%s] in url [%s]' %(image_url, url))
					image_response = get_request_response(image_url)
					if not image_response.ok:
						logging.error('Image [%s] in url [%s] check is [FAILED]' %(image_url, url))
						if url not in failed_images_dict.keys(): failed_images_dict[url] = []
						failed_images_dict[url].append(image_url)
			else:
				logging.error('Page [%d/%d][%s] check is [FAILED]' %(page_count+start, counter, url))
				failed +=1
				main_urls_failed_dict[server].append(url)
		except:
				logging.warning('Category [%d/%d][%s] check is [NOT TESTED]' %(page_count+start, end, url))
				main_urls_not_tested_dict[server].append(url)	
		logging.info('Pages count [%d] and [%d] are SUCCEED and [%d] are pages with FAILED images' %(page_count, succeed, len(failed_images_dict.keys())))

	if main_urls_failed_dict[server]:logging.error('Failed [%d] URLs:%s' %(len(main_urls_failed_dict[server]), str(main_urls_failed_dict[server])))
	if failed_images_dict:
		logging.info('============================')
		logging.info('===========REPORT===========')
		logging.info('============================')
		logging.error('Number of pages has failed images are [%d] with details;' % len(failed_images_dict.keys()))
		for url in failed_images_dict.keys():
			logging.info('+++++++++++New URL++++++++++++')
			logging.info('URL [%s] has [%d] failed images %s' % (url, len(failed_images_dict[url]), str(failed_images_dict[url])))