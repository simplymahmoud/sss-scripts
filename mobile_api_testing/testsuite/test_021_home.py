# -*- coding: utf-8 -*-
from testframework.base import *
import types


response_headers = {'Connection': 'Keep-Alive', 
                    'Cache-Control': 'public, s-maxage=86400', 
                    'Content-Type': 'application/vnd.api+json; charset=utf-8'}

response_body = {'data': ['id', 'type', 'links', 'attributes']}


class TestHome(BaseTest):


    def test001_get_home_page_widget(self):
        """ TestCase-34: Test case for test get /widgets/{id}/products/?.*
        **Test Scenario:**
        #. Get /widgets/{id}/products/?, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_request_response(uri='/widgets/43/products/?page[number]=1&page[size]=8')
        
        self.lg('#. Get /widgets/43/products/?page[number]=1&page[size]=8, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in widgets_response_headers.keys()]
        [self.assertIn(widgets_response_headers[header], response.headers[header]) for header in widgets_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)
        
        [self.assertIn(key, response.json().keys()) for key in  response_body['data'].keys()]
        
        self.lg('%s ENDED' % self._testID) 