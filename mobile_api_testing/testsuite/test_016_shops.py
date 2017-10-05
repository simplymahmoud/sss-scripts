# -*- coding: utf-8 -*-
from testframework.base import *
import types


shops_response_headers = {'Connection': 'Keep-Alive', 
                          'Cache-Control': 'public, s-maxage=86400', 
                          'Content-Type': 'application/vnd.api+json; charset=utf-8'}


class TestShops(BaseTest):


    def test001_get_shops(self):
        """ TestCase-27: Test case for test get /shops.*
        **Test Scenario:**
        #. Get /shops, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/shops')
        
        self.lg('#. Get /shops, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in shops_response_headers.keys()]
        [self.assertEqual(shops_response_headers[header], response.headers[header]) for header in shops_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)
        
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.ListType)

        self.lg('%s ENDED' % self._testID)      