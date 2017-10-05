# -*- coding: utf-8 -*-
from testframework.base import *
import types


subscriptions_response_headers = {'Connection': 'Keep-Alive', 
                                  'Cache-Control': 'public, s-maxage=86400', 
                                  'Content-Type': 'application/vnd.api+json; charset=utf-8'}


class TestSubscriptions(BaseTest):


    def test001_get_subscriptions(self):
        """ TestCase-31: Test case for test get /subscriptions.*
        **Test Scenario:**
        #. Get /subscriptions, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/payments/subscriptions/2?include=charges')
        
        self.lg('#. Get /subscriptions, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in subscriptions_response_headers.keys()]
        [self.assertEqual(subscriptions_response_headers[header], response.headers[header]) for header in subscriptions_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)
        
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)

        self.lg('%s ENDED' % self._testID)      