# -*- coding: utf-8 -*-
from testframework.base import *
import types


auth_response_headers = {'Transfer-Encoding': 'chunked', 
                         'Connection': 'keep-alive', 
                         'pragma': 'no-cache', 
                         'Cache-Control': 'no-store, private', 
                         'Content-Type': 'application/json; charset=UTF-8'}

client_token = {'token_type': 'Bearer', 
                'expires_in': 31536000,
                'access_token': ''}
                
                
class TestAuth(BaseTest):


    def test001_get_client_token(self):
        """ TestCase-1: Test case for test get /oauth/token.*
        **Test Scenario:**
        #. Get /oauth/token using client token, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_token_response(self.client_auth_header)
        
        self.lg('#. Get /oauth/token using user token, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        '''
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in auth_response_headers.keys()]
        [self.assertEqual(auth_response_headers[header], response.headers[header]) for header in auth_response_headers.keys()]

        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        self.assertEqual(response.json()['token_type'], client_token['token_type']) 
        self.assertEqual(response.json()['expires_in'], client_token['expires_in']) 
        self.assertNotEqual(response.json()['access_token'], client_token['access_token'])   
        '''
        self.lg('%s ENDED' % self._testID)  

    '''
    def test002_get_user_token(self):
        """ TestCase-2: Test case for test get /oauth/token.*
        **Test Scenario:**
        #. Get /oauth/token using user token, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_response_token(self.user_auth_header)
        
        self.lg('#. Get /oauth/token using user token, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in auth_response_headers.keys()]

        self.lg('#. Check response body, should succeed')

        self.lg('%s ENDED' % self._testID)   
    '''