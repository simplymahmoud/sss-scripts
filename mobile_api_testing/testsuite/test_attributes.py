# -*- coding: utf-8 -*-
from testframework.base import *
import types


attributes_response_headers = {'Transfer-Encoding': 'chunked', 
                               'Connection': 'keep-alive', 
                               'pragma': 'no-cache', 
                               'Cache-Control': 'private, must-revalidate', 
                               'Content-Type': 'application/vnd.api+json'}

attributes = {
        "type": "attributes",
        "id": "374",
        "attributes": {
            "attribute_id": 374,
            "attribute_code": "nutrition_form",
            "is_required": 0,
            "default_value": "",
            "label": "Nutrition Form",
            "is_visible": 1,
            "is_searchable": 0,
            "is_filterable": 1,
            "is_comparable": 0,
            "position": 0
        },
        "relationships": {
            "options": {
                "data": [],
                "links": {
                    "self": "http://45.33.59.76/api/v1/attributes/374/relationships/options",
                    "related": "http://45.33.59.76/api/v1/attributes/374/options"
                }
            }
        },
        "links": {
            "self": "http://45.33.59.76/api/v1/attributes/374"
        }
    }

no_attributes = 20



class TestAttributes(BaseTest):


    def test001_get_attributes(self):
        """ TestCase-2: Test case for test get /attributes.*
        **Test Scenario:**
        #. Get /attributes, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/attributes')
        
        self.lg('#. Get /attributes, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        '''
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in attributes_response_headers.keys()]
        [self.assertEqual(attributes_response_headers[header], response.headers[header]) for header in attributes_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.ListType)
        self.assertEqual(len(response.json()['data']), no_attributes)
        [self.assertEqual(type(attributes_dict), types.DictType) for attributes_dict in response.json()['data']]

        for attributes_dict in response.json()['data']:
            for key in attributes_dict.keys():
                self.assertIn(key, attributes.keys())
            if attributes_dict['id'] == attributes['id']:
               self.assertEqual(attributes_dict['type'], attributes['type']) 
               self.assertEqual(attributes_dict['relationships'], attributes['relationships']) 
               self.assertEqual(attributes_dict['links'], attributes['links']) 
        '''
        self.lg('%s ENDED' % self._testID)                        
        

    def test002_get_attribute(self):
        """ TestCase-3: Test case for test get /attributes/{id}.*
        **Test Scenario:**
        #. Get /attributes/{id}, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_request_response(uri='/attributes/%s' % attributes['id'])
        
        self.lg('#. Get /attributes/{id}, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        '''
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in attributes_response_headers.keys()]
        [self.assertIn(attributes_response_headers[header], response.headers[header]) for header in attributes_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)
        self.assertEqual(response.json()['data']['id'], attributes['id']) 
        self.assertEqual(response.json()['data']['type'], attributes['type']) 
        self.assertEqual(response.json()['data']['links'], attributes['links']) 
        self.assertEqual(response.json()['data']['relationships'], attributes['relationships'])         
        '''
        self.lg('%s ENDED' % self._testID)