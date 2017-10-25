from sys import argv
import time
import os
import logging
from datetime import datetime
import csv
import gdata.docs.client
import gspread
import os
import sys

username = 'sunandsandsportsdocs@gmail.com'
password = 'SunandSandSportsTesting'
google_docs_folder_id = 'Speed Results'


def create_spreadsheet():

    document_title = 'Generated %s' % datetime.now().strftime('%Y-%m-%d')

    docs_client = gdata.docs.client.DocsClient()
    docs_client.ClientLogin(username, password, 'Any non empty string')
    document = gdata.docs.data.Resource(type='spreadsheet', title=document_title)
    resource = docs_client.CreateResource(document)

    docs_client.MoveResource(resource, docs_client.GetResourceById(google_docs_folder_id))

    full_id = resource.resource_id.text # returned by gdata
    gc = gspread.login(username, password)
    gc_id = full_id[len('spreadsheet:'):]

    return gc.open_by_key(gc_id)


def main():

	if len(argv) < 2:
		raise AssertionError("Usage: python csv-google-docs-uploader.py sitemap.csv ... ex. python csv-google-docs-uploader.py sitemap_ae_en.csv")


	csv_file = argv[1]
	file_path = os.path.abspath(csv_file)

	fh = open(file_path, 'rt')

	try:
		reader = csv.DictReader(fh)
	except IOError:
		raise ScriptError('unable to read csv file: csv_file=csv_file')
	finally:
		sh = create_spreadsheet()
        ws = sh.get_worksheet(0)	

        column_count = 1
        row_count = 1

        headers_printed = False
        for row in reader:
            for data in row.keys():
                if not headers_printed:
                    for header in list(row.keys()):
                        ws.update_cell(column_count, row_count, header)
                        row_count += 1
                    row_count = 1
                    column_count += 1
                    headers_printed = True
                ws.update_cell(column_count, row_count, row[data])
                row_count += 1
            column_count += 1
            row_count = 1

        fh.close()        


if __name__ == '__main__':        
	sys.exit(main())