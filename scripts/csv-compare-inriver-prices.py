from sys import argv
import time
import os
import logging


def get_file_content_list(file_path):
	input = open(file_path, 'r')
	lines = input.readlines()
	splitted_lines = [line.split(',') for line in lines]
	return splitted_lines

def get_sku_from_inriver_line(inriver_line):
	sku = inriver_line[2]
	return sku

def get_prices_line_using_sku(prices_lines, sku):
	for prices_line in prices_lines:
		if sku in prices_line:
			return prices_line
	return []

def get_inriver_line_using_sku(inriver_lines, sku):
	for inriver_line in inriver_lines:
		if sku in inriver_line:
			return inriver_line
	return []	

def compare_inriver_line_with_prices_line(inriver_line, prices_line):	
	if inriver_line[12] != '0' and inriver_line[12] != prices_line[1]: 
		logging.error('AED prices are not match [%s] and [%s]' %(str(inriver_line[12]), str(prices_line[1])))
		return False #Check AED
	if inriver_line[36] != '0' and inriver_line[36] != prices_line[4]: 
		logging.error('SAR prices are not match [%s] and [%s]' %(str(inriver_line[36]), str(prices_line[4])))
		return False #Check SAR
	if inriver_line[37] != '0' and inriver_line[37] != prices_line[7]: 
		logging.error('KWD prices are not match [%s] and [%s]' %(str(inriver_line[37]), str(prices_line[7])))
		return False #Check KWD
	if inriver_line[40] != '0' and inriver_line[40] != prices_line[10]: 
		logging.error('QAR prices are not match [%s] and [%s]' %(str(inriver_line[40]), str(prices_line[10])))
		return False #Check QAR
	if inriver_line[61] != '0' and inriver_line[61] != prices_line[13]: 
		logging.error('USD prices are not match [%s] and [%s]' %(str(inriver_line[61]), str(prices_line[13])))
		return False #Check USD
	
	#if inriver_line[51] != '0' and inriver_line[51] != '' and (inriver_line[51] != prices_line[2] or inriver_line[51] != prices_line[3]): 
	if inriver_line[51] != '0' and inriver_line[51] != '' and inriver_line[51] != prices_line[3]: 
		logging.error('AED prices are not match [%s] with discount/final [%s]/[%s]' %(str(inriver_line[51]), str(prices_line[2]), str(prices_line[3])))
		return False #Check AED discount/final
	#if inriver_line[52] != '0' and inriver_line[52] != '' and (inriver_line[52] != prices_line[5] or inriver_line[52] != prices_line[6]): 
	if inriver_line[52] != '0' and inriver_line[52] != '' and inriver_line[52] != prices_line[6]: 
		logging.error('SAR prices are not match [%s] with discount/final [%s]/[%s]' %(str(inriver_line[52]), str(prices_line[5]), str(prices_line[6])))
		return False #Check SAR discount/final
	#if inriver_line[53] != '0' and inriver_line[53] != '' and (inriver_line[53] != prices_line[8] or inriver_line[53] != prices_line[9]): 
	if inriver_line[53] != '0' and inriver_line[53] != '' and inriver_line[53] != prices_line[9]: 
		logging.error('KWD prices are not match [%s] with discount/final [%s]/[%s]' %(str(inriver_line[53]), str(prices_line[8]), str(prices_line[9])))
		return False #Check KWD discount/final
	#if inriver_line[56] != '0' and inriver_line[56] != '' and (inriver_line[56] != prices_line[11] or inriver_line[56] != prices_line[12]): 
	if inriver_line[56] != '0' and inriver_line[56] != '' and inriver_line[56] != prices_line[12]: 
		logging.error('QAR prices are not match [%s] with discount/final [%s]/[%s]' %(str(inriver_line[56]), str(prices_line[11]), str(prices_line[12])))
		return False #Check QAR discount/final
	#if inriver_line[62] != '0' and inriver_line[62] != '' and (inriver_line[62] != prices_line[14] or inriver_line[62] != prices_line[15]): 
	if inriver_line[62] != '0' and inriver_line[62] != '' and inriver_line[62] != prices_line[15]: 
		logging.error('USD prices are not match [%s] with discount/final [%s]/[%s]' %(str(inriver_line[62]), str(prices_line[14]), str(prices_line[15])))
		return False #Check USD discount/final
	
	return True

def generate_csv_file_with_the_failed_skus(failed_skus):
	logging.info('Generating CSV with failed SKUs..')
	file_path = inriver_file_path + '-failed-sku.csv'
	output = open(file_path, 'w')		
	output.write('sku,AED Magento,AED Inriver,AED Magento Discount,AED Inriver Discount,AED Magento Final,SAR Magento,SAR Inriver,SAR Magento Discount,SAR Inriver Discount,SAR Magento Final,KWD Magento,KWD Inriver,KWD Magento Discount,KWD Inriver Discount,KWD Magento Final,QAR Magento,QAR Inriver,QAR Magento Discount,QAR Inriver Discount,QAR Magento Final,USD Magento,USD Inriver,USD Magento Discount,USD Inriver Discount,USD Magento Final\n')
	for sku in failed_skus:
		inriver_line = get_inriver_line_using_sku(inriver_lines=inriver_lines, sku=sku)
		prices_line = get_prices_line_using_sku(prices_lines=prices_lines, sku=sku)	
		
		AED_Inriver = inriver_line[12]
		SAR_Inriver = inriver_line[36]
		KWD_Inriver = inriver_line[37]
		QAR_Inriver = inriver_line[40]
		USD_Inriver = inriver_line[61]

		AED_Magento = prices_line[1]
		SAR_Magento = prices_line[4]
		KWD_Magento = prices_line[7]
		QAR_Magento = prices_line[10]
		USD_Magento = prices_line[13]

		AED_Inriver_Discount = inriver_line[51]
		SAR_Inriver_Discount = inriver_line[52]
		KWD_Inriver_Discount = inriver_line[53]
		QAR_Inriver_Discount = inriver_line[56]
		USD_Inriver_Discount = inriver_line[62]

		AED_Magento_Discount = prices_line[2]
		SAR_Magento_Discount = prices_line[5]
		KWD_Magento_Discount = prices_line[8]
		QAR_Magento_Discount = prices_line[11]
		USD_Magento_Discount = prices_line[14]

		AED_Magento_Final = prices_line[3]
		SAR_Magento_Final = prices_line[6]
		KWD_Magento_Final = prices_line[9]
		QAR_Magento_Final = prices_line[12]
		USD_Magento_Final = prices_line[15]
		
		line = sku + ',' + AED_Magento + ',' + AED_Inriver + ',' + AED_Magento_Discount + ',' + AED_Inriver_Discount + ',' + AED_Magento_Final + ',' + SAR_Magento + ',' + SAR_Inriver + ',' + SAR_Magento_Discount + ',' + SAR_Inriver_Discount + ',' + SAR_Magento_Final + ',' + KWD_Magento + ',' + KWD_Inriver + ',' + KWD_Magento_Discount + ',' + KWD_Inriver_Discount + ',' + KWD_Magento_Final + ',' + QAR_Magento + ',' + QAR_Inriver + ',' + QAR_Magento_Discount + ',' + QAR_Inriver_Discount + ',' + QAR_Magento_Final + ',' + USD_Magento + ',' + USD_Inriver + ',' + USD_Magento_Discount + ',' + USD_Inriver_Discount + ',' + USD_Magento_Final + '\n'
		output.write(line)
	output.close()

if __name__ == '__main__':
	if len(argv) < 3:
		raise AssertionError("Usage: python csv-copmare-inriver-prices.py inriver.csv prices.csv")
	
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
	failed_skus = []
	not_found_skus = []
	previous_sku = ''
	for inriver_line in inriver_lines:
		counter += 1
		logging.info('Processing inriver line [%d/%d]' %(counter, inriver_lines_counter))	
		inriver_sku = get_sku_from_inriver_line(inriver_line=inriver_line)
		if inriver_sku == previous_sku:
			continue
		logging.info('Found SKU is [%s]' %(inriver_sku))
		previous_sku = inriver_sku
		prices_line = get_prices_line_using_sku(prices_lines=prices_lines, sku=inriver_sku)	
		if prices_line == []: 
			logging.error('SKU %s [NOT FOUND]' %inriver_sku)
			not_found_skus.append(inriver_sku)
			continue
		prices_line[-1] = prices_line[-1].replace('\n','')	
		if compare_inriver_line_with_prices_line(inriver_line, prices_line):
			logging.info('SKU %s [Succeed]' %inriver_sku)			
		else:
			logging.info('Comparing items from revier line {%s} with prices line {%s}' %(inriver_line, prices_line))
			logging.error('SKU %s [Failed]' %inriver_sku)
			failed_skus.append(inriver_sku)

		if counter%100 == 0:
			if not_found_skus:
				logging.error('Not found SKUs are %s' %str(not_found_skus))

			if failed_skus:
				logging.error('Failed SKUs are %s' %str(failed_skus))
				generate_csv_file_with_the_failed_skus(failed_skus)

		
	if not_found_skus:
		logging.error('Not found SKUs are %s' %str(not_found_skus))

	if failed_skus:
		logging.error('Failed SKUs are %s' %str(failed_skus))
		generate_csv_file_with_the_failed_skus(failed_skus)
