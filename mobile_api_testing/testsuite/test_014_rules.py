# -*- coding: utf-8 -*-
from testframework.base import *
import types


rules_response_headers = {'Connection': 'Keep-Alive', 
                          'Cache-Control': 'public, s-maxage=86400', 
                          'Content-Type': 'application/vnd.api+json; charset=utf-8'}

rules = {
        "type": "rules",
        "id": "7",
        "attributes": {
            "object": "App\\Models\\V1\\Magento\\Product\\Product",
            "args": "a:2:{s:11:\"category_id\";i:3;s:5:\"limit\";i:6;}",
            "created_at": "2017-09-26 17:23:32",
            "updated_at": "2017-09-26 17:23:32"
        },
        "links": {
            "self": "https://api-staging.sssports.com/v1/rules/7"
        }}

no_rules = 2


class TestFiles(BaseTest):


    def test001_get_rules(self):
        """ TestCase-23: Test case for test get /rules.*
        **Test Scenario:**
        #. Get /rules, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/rules')
        
        self.lg('#. Get /rules, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in rules_response_headers.keys()]
        [self.assertEqual(rules_response_headers[header], response.headers[header]) for header in rules_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)

        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.ListType)
        self.assertEqual(len(response.json()['data']), no_rules)
        [self.assertEqual(type(file_dict), types.DictType) for file_dict in response.json()['data']]

        for category_dict in response.json()['data']:
            for key in category_dict.keys():
                self.assertIn(key, rules.keys())
            if file_dict['id'] == rules['id']:
               self.assertEqual(file_dict['type'], rules['type']) 
               self.assertEqual(file_dict['links'], rules['links']) 
               self.assertEqual(file_dict['attributes'], rules['attributes']) 

        self.lg('%s ENDED' % self._testID)                        
        

    def test002_get_rule(self):
        """ TestCase-24: Test case for test get /rules/{id}.*
        **Test Scenario:**
        #. Get /rules/{id}, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_request_response(uri='/rules/%s' % rules['id'])
        
        self.lg('#. Get /rules/{id}, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in rules_response_headers.keys()]
        [self.assertIn(rules_response_headers[header], response.headers[header]) for header in rules_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)
        self.assertEqual(response.json()['data']['id'], rules['id']) 
        self.assertEqual(response.json()['data']['type'], rules['type']) 
        self.assertEqual(response.json()['data']['links'], rules['links']) 
        self.assertEqual(response.json()['data']['attributes'], rules['attributes'])         

        self.lg('%s ENDED' % self._testID)