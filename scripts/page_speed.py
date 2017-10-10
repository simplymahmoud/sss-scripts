from sys import argv
import pycurl
import certifi
import time
import os
import logging


def get_page(url):
	curl = pycurl.Curl()
	curl.setopt(pycurl.CAINFO, certifi.where())
	curl.setopt(pycurl.URL, url)                    #set url
	curl.setopt(pycurl.FOLLOWLOCATION, 1)  
	content = curl.perform()                        #execute 
	dns_time = curl.getinfo(pycurl.NAMELOOKUP_TIME) #DNS time
	conn_time = curl.getinfo(pycurl.CONNECT_TIME)   #TCP/IP 3-way handshaking time
	ttfb = curl.getinfo(pycurl.STARTTRANSFER_TIME)  #time-to-first-byte time
	total_time = curl.getinfo(pycurl.TOTAL_TIME)    #last requst time
 	curl.close()
	return {'DNS Time': dns_time, 'Connection Time': conn_time, 'TTFB': ttfb, 'Total Time': total_time}


if __name__ == '__main__':
	if len(argv) < 2:
		raise AssertionError("Usage: python page_speed.py url ... ex. python page_speed.py https://en-ae.sssports.com ")
	
	url = argv[1]

	if not os.path.exists('logs'):
		os.mkdir('logs')
	log_path = os.path.abspath('logs')
	log_file = os.path.join(log_path, 'page-speed-' + str(time.time()) + '.log')
	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename=log_file,level=logging.DEBUG)
	logging.info('Page speed check on page [%s]' %url)
	page_speed = get_page(url)
	logging.info('============================')
	logging.info('===========REPORT===========')
	logging.info('============================')
	keys = ['DNS Time', 'Connection Time', 'TTFB', 'Total Time']
	[logging.info(key + ': ' + str(page_speed[key])) for key in keys]
	print '\n============================'
	print '===========REPORT==========='
	print '============================'
	for key in keys:
		print key + ': ' + str(page_speed[key])