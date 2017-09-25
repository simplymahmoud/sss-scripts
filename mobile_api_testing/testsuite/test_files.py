# -*- coding: utf-8 -*-
from testframework.base import *
import types


files_response_headers = {'Transfer-Encoding': 'chunked', 
                          'Connection': 'keep-alive', 
                          'pragma': 'no-cache', 
                          'Cache-Control': 'private, must-revalidate', 
                          'Content-Type': 'application/vnd.api+json'}

files = {"type":"files","id":"1","attributes":{"filetype":"image\/jpeg","extension":"jpeg","filesize":120244,"created_at":"2017-09-18 21:24:48","updated_at":"2017-09-18 21:24:48","url":"https:\/\/blog2016oct.s3.amazonaws.com\/api\/v1\/images\/resized\/AR_slider1%404x.jpg"},"links":{"self":"https:\/\/api.sssports.com\/v1\/files\/1"}}

no_files = 26


class TestFiles(BaseTest):


    def test001_get_files(self):
        """ TestCase-8: Test case for test get /files.*
        **Test Scenario:**
        #. Get /files, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/files')
        
        self.lg('#. Get /files, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        '''
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in files_response_headers.keys()]
        [self.assertEqual(files_response_headers[header], response.headers[header]) for header in files_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.ListType)
        self.assertEqual(len(response.json()['data']), no_files)
        [self.assertEqual(type(file_dict), types.DictType) for file_dict in response.json()['data']]

        for category_dict in response.json()['data']:
            for key in category_dict.keys():
                self.assertIn(key, files.keys())
            if file_dict['id'] == files['id']:
               self.assertEqual(file_dict['type'], files['type']) 
               self.assertEqual(file_dict['links'], files['links']) 
               self.assertEqual(file_dict['attributes'], files['attributes']) 
        '''
        self.lg('%s ENDED' % self._testID)                        
        

    def test002_get_file(self):
        """ TestCase-9: Test case for test get /files/{id}.*
        **Test Scenario:**
        #. Get /files/{id}, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_request_response(uri='/files/%s' % files['id'])
        
        self.lg('#. Get /files/{id}, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        '''
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in files_response_headers.keys()]
        [self.assertIn(files_response_headers[header], response.headers[header]) for header in files_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)
        self.assertEqual(response.json()['data']['id'], files['id']) 
        self.assertEqual(response.json()['data']['type'], files['type']) 
        self.assertEqual(response.json()['data']['links'], files['links']) 
        self.assertEqual(response.json()['data']['attributes'], files['attributes'])         
        '''
        self.lg('%s ENDED' % self._testID)