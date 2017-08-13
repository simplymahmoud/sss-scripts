from sys import argv
import requests
import time
import os
import logging


def head_request_response(url):
	session = requests.Session()
	response = session.head(url, timeout=60)	
	session.close()
	return response

def get_site_urls_list(file_path):
	input = open(file_path, 'r')
	lines = input.readlines()
	input.close()
	urls = []
	for line in lines:
		if line.count('"')==0:
			urls.append('https://' + line.split(',')[-2])
		else:
			urls.append('https://' + line.split('"')[1])
	#urls = [url.split('.')[0] + '-upgrade' + url[len(url.split('.')[0]):] for url in urls]
	return urls


if __name__ == '__main__':
	if len(argv) < 2:
		raise AssertionError("Usage: python csv-layerednav-getter.py layerednav.csv start[optional] end[optional] ... ex. python csv-layerednav-getter.py layerednav.csv 0 10")
	
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

	succeed = 0
	failed = 0
	not_tested = 0
	page_count = 0

	if not os.path.exists('logs'):
		os.mkdir('logs')
	log_path = os.path.abspath('logs')
	log_file = os.path.join(log_path, server + '-layerednav-' + str(time.time()) + '.log')
	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename=log_file,level=logging.DEBUG)
	logging.info('Health check on csv [%s] layered nav' %server)
	logging.info('Found [%d] page in [%s]' %(counter, server))
	
	for url in urls[start:end]:
		page_count +=1
		try:
			response = head_request_response(url)
			
			if response.ok:
				logging.info('Page [%d/%d][%s] check is [SUCCEED]' % (page_count+start, counter, url))
				succeed +=1
			else:
				logging.error('Page [%d/%d][%s] check is [FAILED]' %(page_count+start, counter, url))
				failed +=1
				main_urls_failed_dict[server].append(url)
		except:
				logging.warning('Page [%d/%d][%s] check is [NOT TESTED]' %(page_count+start, counter, url))
				not_tested +=1
				main_urls_not_tested_dict[server].append(url)	
		
		logging.info('Pages count [%d] and [%d] are SUCCEED and [%d] are FAILED and [%d] are NOT TESTED' %(page_count, succeed, failed, not_tested))

	if main_urls_not_tested_dict[server]:logging.warning('Not Tested [%d] URLs:%s' %(len(main_urls_not_tested_dict[server]), str(main_urls_not_tested_dict[server])))
	if main_urls_failed_dict[server]:logging.error('Failed [%d] URLs:%s' %(len(main_urls_failed_dict[server]), str(main_urls_failed_dict[server])))