from sys import argv
import requests
import pycurl
import certifi
import StringIO
import time
import os
import logging
import datetime
import urllib


def get_xml_sitemap_file(file_name):
	urllib.urlretrieve("https://sssports.com/pub/sitemap/" + file_name, file_name)

def head_request_response(url):
	session = requests.Session()
	response = session.head(url, timeout=30, allow_redirects=False)	
	session.close()
	return response

def get_site_urls_list(file_path):
	input = open(file_path, 'r')
	data = input.readlines()
	temp_urls = [url.replace('<url><loc>', '') for url in data if url.count('<loc>')]
	urls = []
	for temp_url in temp_urls:		
		urls.append(temp_url.split('</loc>')[0])

	return urls

def get_page(url):
	block = StringIO.StringIO()
	curl = pycurl.Curl()
	curl.setopt(pycurl.WRITEFUNCTION, block.write)
	curl.setopt(pycurl.CAINFO, certifi.where())
	curl.setopt(pycurl.URL, url)                    #set url
	curl.setopt(pycurl.FOLLOWLOCATION, 1)  
	content = curl.perform()                        #execute 
	#time_stamp = time.time()	
	dns_time = str(curl.getinfo(pycurl.NAMELOOKUP_TIME)) #DNS time
	conn_time = str(curl.getinfo(pycurl.CONNECT_TIME))   #TCP/IP 3-way handshaking time
	ttfb = str(curl.getinfo(pycurl.STARTTRANSFER_TIME))  #time-to-first-byte time
	total_time = str(curl.getinfo(pycurl.TOTAL_TIME))    #last requst time
 	curl.close()
 	standard_time = str(datetime.datetime.now())#datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
	return {'DNS Time': dns_time, 'Connection Time': conn_time, 'TTFB': ttfb, 'Total Time': total_time, 'URL': url, 'Time Stamp': standard_time}

def generate_csv_file_with_speeds(urls_with_speed):
	logging.info('Generating CSV with URL speeds...')
	file_path = log_file + '-speeds.csv'
	output = open(file_path, 'w')
	output.write('Time Stamp,URL,DNS Time,Connection Time,TTFB,Total Time\n')
	for url_speed in urls_with_speed:
		output.write(url_speed['Time Stamp'] + ',' + url_speed['URL'] + ',' + url_speed['DNS Time'] + ',' + url_speed['Connection Time'] + ',' + url_speed['TTFB'] + ',' + url_speed['Total Time'] + '\n')
	output.close()
	logging.info('Generating CSV with URL speeds [DONE].')

if __name__ == '__main__':
	
	server = 'sitemap_ae_en.xml'
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

	urls_speeds_list = []

	succeed = 0
	failed = 0
	not_tested = 0
	page_count = 0

	if not os.path.exists('logs'):
		os.mkdir('logs')
	log_path = os.path.abspath('logs')
	log_file = os.path.join(log_path, server + '-speed-' + str(time.time()) + '.log')
	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename=log_file,level=logging.DEBUG)
	logging.info('Health check on server [%s] sitemap' %server)
	logging.info('Found [%d] page in [%s]' %(counter, server))
	
	for url in urls[start:end]:
		page_count +=1
		try:
			response = head_request_response(url)			
			if response.ok:
				logging.info('Page [%d/%d][%s] check is [SUCCEED]' % (page_count+start, counter, url))
				succeed +=1
				page_speed = get_page(url)
				logging.info('Page speed is %s' % str(page_speed))
				urls_speeds_list.append(page_speed)
			else:
				logging.error('Page [%d/%d][%s] check is [FAILED]' %(page_count+start, counter, url))
				failed +=1
				main_urls_failed_dict[server].append(url)
		except:
				logging.warning('Page [%d/%d][%s] check is [NOT TESTED]' %(page_count+start, counter, url))
				not_tested +=1
				main_urls_not_tested_dict[server].append(url)	
		
		logging.info('Pages count [%d] and [%d] are SUCCEED and [%d] are FAILED and [%d] are NOT TESTED' %(page_count, succeed, failed, not_tested))

		if page_count%100 == 0:
			if main_urls_not_tested_dict[server]:logging.warning('Not Tested [%d] URLs:%s' %(len(main_urls_not_tested_dict[server]), str(main_urls_not_tested_dict[server])))
			if main_urls_failed_dict[server]:logging.error('Failed [%d] URLs:%s' %(len(main_urls_failed_dict[server]), str(main_urls_failed_dict[server])))
	
	if main_urls_not_tested_dict[server]:logging.warning('Not Tested [%d] URLs:%s' %(len(main_urls_not_tested_dict[server]), str(main_urls_not_tested_dict[server])))
	if main_urls_failed_dict[server]:logging.error('Failed [%d] URLs:%s' %(len(main_urls_failed_dict[server]), str(main_urls_failed_dict[server])))
	generate_csv_file_with_speeds(urls_with_speed=urls_speeds_list)

