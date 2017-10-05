       # -*- coding: utf-8 -*-
from testframework.base import *
import types


orders_response_headers = {'Connection': 'Keep-Alive', 
                           'Cache-Control': 'public, s-maxage=86400', 
                           'Content-Type': 'application/vnd.api+json; charset=utf-8'}


class TestOrders(BaseTest):

    def test001_get_order(self):
        """ TestCase-19: Test case for test get /orders/{id}.*
        **Test Scenario:**
        #. Get /orders/{id}, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_request_response(uri='/orders/1')
        
        self.lg('#. Get /orders/{id}, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in orders_response_headers.keys()]
        [self.assertIn(orders_response_headers[header], response.headers[header]) for header in orders_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  

        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)

        self.lg('%s ENDED' % self._testID)                 