from sys import argv
import time
import os
import logging


def get_file_content_list(file_path):
	input = open(file_path, 'r')
	lines = input.readlines()
	splitted_lines = [line.split(',') for line in lines]
	return splitted_lines

def get_item_number_from_inriver_line(inriver_line):
	item_number = inriver_line[2]
	return item_number

def get_prices_line_using_sku(prices_lines, item_number):
	for prices_line in prices_lines:
		if item_number in prices_line:
			return prices_line
	return []

def compare_inriver_line_with_prices_line(inriver_line, prices_line):	
	if inriver_line[12] != '0' and inriver_line[12] != prices_line[50]: 
		logging.error('AED prices are not match [%s] and [%s]' %(str(inriver_line[12]), str(prices_line[50])))
		return False #Check AED
	if inriver_line[36] != '0' and inriver_line[36] != prices_line[150]: 
		logging.error('SAR prices are not match [%s] and [%s]' %(str(inriver_line[36]), str(prices_line[150])))
		return False #Check SAR
	if inriver_line[37] != '0' and inriver_line[37] != prices_line[151]: 
		logging.error('KWD prices are not match [%s] and [%s]' %(str(inriver_line[37]), str(prices_line[151])))
		return False #Check KWD
	if inriver_line[40] != '0' and inriver_line[40] != prices_line[154]: 
		logging.error('QAR prices are not match [%s] and [%s]' %(str(inriver_line[40]), str(prices_line[154])))
		return False #Check QAR
	if inriver_line[61] != '0' and inriver_line[61] != prices_line[179]: 
		logging.error('USD prices are not match [%s] and [%s]' %(str(inriver_line[61]), str(prices_line[179])))
		return False #Check USD
	#if inriver_line[51] != '0' and inriver_line[51] != '' and (inriver_line[51] != prices_line[2] or inriver_line[51] != prices_line[3]): 
	if inriver_line[51] != '0' and inriver_line[51] != '' and inriver_line[51] != prices_line[168]: 
		logging.error('AED prices are not match [%s] with discount [%s]' %(str(inriver_line[51]), str(prices_line[168])))
		return False #Check AED discount/final
	#if inriver_line[52] != '0' and inriver_line[52] != '' and (inriver_line[52] != prices_line[5] or inriver_line[52] != prices_line[6]): 
	if inriver_line[52] != '0' and inriver_line[52] != '' and inriver_line[52] != prices_line[167]: 
		logging.error('SAR prices are not match [%s] with discount [%s]' %(str(inriver_line[52]), str(prices_line[167])))
		return False #Check SAR discount/final
	#if inriver_line[53] != '0' and inriver_line[53] != '' and (inriver_line[53] != prices_line[8] or inriver_line[53] != prices_line[9]): 
	if inriver_line[53] != '0' and inriver_line[53] != '' and inriver_line[53] != prices_line[169]: 
		logging.error('KWD prices are not match [%s] with discount [%s]' %(str(inriver_line[53]), str(prices_line[169])))
		return False #Check KWD discount/final
	#if inriver_line[56] != '0' and inriver_line[56] != '' and (inriver_line[56] != prices_line[11] or inriver_line[56] != prices_line[12]): 
	if inriver_line[56] != '0' and inriver_line[56] != '' and inriver_line[56] != prices_line[172]: 
		logging.error('QAR prices are not match [%s] with discount [%s]' %(str(inriver_line[56]), str(prices_line[172])))
		return False #Check QAR discount/final
	#if inriver_line[62] != '0' and inriver_line[62] != '' and (inriver_line[62] != prices_line[14] or inriver_line[62] != prices_line[15]): 
	if inriver_line[62] != '0' and inriver_line[62] != '' and inriver_line[62] != prices_line[180]: 
		logging.error('USD prices are not match [%s] with discount [%s]' %(str(inriver_line[62]), str(prices_line[180])))
		return False #Check USD discount/final
	
	return True

if __name__ == '__main__':
	if len(argv) < 3:
		raise AssertionError("Usage: python csv-copmare-inriver-discounts.py inriver.csv discounts.csv")
	
	inriver = argv[1]
	inriver_file_path = os.path.abspath(inriver)
	
	prices = argv[2]
	prices_file_path = os.path.abspath(prices)


	if not os.path.exists('logs'):
		os.mkdir('logs')
	log_path = os.path.abspath('logs')
	log_file = os.path.join(log_path, inriver + '-inriver-' + str(time.time()) + '.log')
	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename=log_file, level=logging.DEBUG)
	logging.info('Compare prices for inriver file [%s] and prices file [%s]' %(inriver, prices))
	

	inriver_lines = get_file_content_list(inriver_file_path)
	inriver_lines_counter = len(inriver_lines)
	logging.info('Found [%d] line in inriver file [%s]' %(inriver_lines_counter, inriver))
	prices_lines = get_file_content_list(prices_file_path)
	logging.info('Found [%d] line in prices file [%s]' %(len(prices_lines), prices))

	counter = 0
	failed_item_numbers = []
	not_found_item_numbers = []
	for inriver_line in inriver_lines:
		counter += 1
		logging.info('Processing inriver line [%d/%d]' %(counter, inriver_lines_counter))
		inriver_item_number = get_item_number_from_inriver_line(inriver_line=inriver_line)
		logging.info('Found item number is [%s]' %(inriver_item_number))
		
		prices_line = get_prices_line_using_sku(prices_lines=prices_lines, item_number=inriver_item_number)	
		if prices_line == []: 
			logging.error('item number %s [NOT FOUND]' %inriver_item_number)
			not_found_skus.append(inriver_item_number)
			continue
		prices_line[-1] = prices_line[-1].replace('\n','')
		if compare_inriver_line_with_prices_line(inriver_line, prices_line):
			logging.info('item number %s [Succeed]' %inriver_item_number)
		else:
			logging.info('Comparing items from revier line {%s} with prices line {%s}' %(inriver_line, prices_line))
			logging.error('item number %s [Failed]' %inriver_item_number)
			failed_skus.append(inriver_sku)

			if counter%100 == 0:
				if not_found_item_numbers:
					logging.error('Not found item numbers are %s' %str(not_found_item_numbers))
				if failed_item_numbers:
					logging.error('Failed item numbers are %s' %str(failed_item_numbers))

	if not_found_item_numbers:
		logging.error('Not found item numbers are %s' %str(not_found_item_numbers))

	if failed_item_numbers:
		logging.error('Failed item numbers are %s' %str(failed_item_numbers))
