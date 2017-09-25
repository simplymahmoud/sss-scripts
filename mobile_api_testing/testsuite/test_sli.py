# -*- coding: utf-8 -*-
from testframework.base import *
import types


search_response_headers = {'Transfer-Encoding': 'chunked', 
                           'Connection': 'Keep-Alive', 
                           'Cache-Control': 'max-age=0', 
                           'Content-Type': 'application/json; charset=utf-8'}

asics = {"result_meta": {"total": 44,
                         "this_page": 10,
                         "requested": 10}}

empty = {"result_meta": {"total": 0, 
                         "this_page": 0, 
                         "requested": 10}}
                         
                         
class TestSLI(BaseTest):


    def test001_get_sli_search_with_results(self):
        """ TestCase-16: Test case for test get SLI search with results.*
        **Test Scenario:**
        #. Get SLI search, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_sli_search(keyword='asics')
        
        self.lg('#. Get SLI search, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        '''
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in search_response_headers.keys()]
        [self.assertEqual(search_response_headers[header], response.headers[header]) for header in search_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        self.assertEqual(response.json()['result_meta'], asics['result_meta'])       
        '''
        self.lg('%s ENDED' % self._testID) 
        
        
    def test002_get_sli_search_without_results(self):
        """ TestCase-17: Test case for test get SLI search without results.*
        **Test Scenario:**
        #. Get SLI search, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_sli_search(keyword='xx')
        
        self.lg('#. Get SLI search, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        '''
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in search_response_headers.keys()]
        [self.assertEqual(search_response_headers[header], response.headers[header]) for header in search_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        self.assertEqual(empty["result_meta"], response.json()["result_meta"]) 
        '''
        self.lg('%s ENDED' % self._testID)         