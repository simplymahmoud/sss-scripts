# -*- coding: utf-8 -*-
from testframework.base import *
import types


blocks_response_headers = {'Transfer-Encoding': 'chunked', 
                           'Connection': 'keep-alive', 
                           'pragma': 'no-cache', 
                           'Cache-Control': 'private, must-revalidate', 
                           'Content-Type': 'application/vnd.api+json'}

womens = {"type":"blocks","id":"1","attributes":{"widget_id":1,"index":0,"label":"Women","text":'',"video":'',"created_at":"2017-09-18 21:24:57","updated_at":"2017-09-18 21:24:57","image_url":"https:\/\/blog2016oct.s3.amazonaws.com\/api\/v1\/images\/resized\/women%404x.jpg","actions_count":1},"relationships":{"actions":{"data":[{"type":"actions","id":"1"}],"links":{"self":"https:\/\/api.sssports.com\/v1\/blocks\/1\/relationships\/actions","related":"https:\/\/api.sssports.com\/v1\/blocks\/1\/actions"}},"file":{"data":{"type":"files","id":"18"},"links":{"self":"https:\/\/api.sssports.com\/v1\/blocks\/1\/relationships\/file","related":"https:\/\/api.sssports.com\/v1\/blocks\/1\/file"}},"rules":{"data":[],"links":{"self":"https:\/\/api.sssports.com\/v1\/blocks\/1\/relationships\/rules","related":"https:\/\/api.sssports.com\/v1\/blocks\/1\/rules"}}},"links":{"self":"https:\/\/api.sssports.com\/v1\/blocks\/1"}}

no_blocks = 92



class TestBlocks(BaseTest):


    def test001_get_blocks(self):
        """ TestCase-2: Test case for test get /blocks.*
        **Test Scenario:**
        #. Get /blocks, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/blocks')
        
        self.lg('#. Get /blocks, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        '''
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in blocks_response_headers.keys()]
        [self.assertEqual(blocks_response_headers[header], response.headers[header]) for header in blocks_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.ListType)
        self.assertEqual(len(response.json()['data']), no_blocks)
        [self.assertEqual(type(blocks_dict), types.DictType) for blocks_dict in response.json()['data']]

        for blocks_dict in response.json()['data']:
            for key in blocks_dict.keys():
                self.assertIn(key, womens.keys())
            if blocks_dict['id'] == womens['id']:
               self.assertEqual(blocks_dict['type'], womens['type']) 
               self.assertEqual(blocks_dict['relationships'], womens['relationships']) 
               self.assertEqual(blocks_dict['links'], womens['links']) 
        '''
        self.lg('%s ENDED' % self._testID)                        
        

    def test002_get_block(self):
        """ TestCase-3: Test case for test get /blocks/{id}.*
        **Test Scenario:**
        #. Get /blocks/{id}, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_request_response(uri='/blocks/%s' % womens['id'])
        
        self.lg('#. Get /blocks/{id}, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        '''
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in blocks_response_headers.keys()]
        [self.assertIn(blocks_response_headers[header], response.headers[header]) for header in blocks_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)
        self.assertEqual(response.json()['data']['id'], womens['id']) 
        self.assertEqual(response.json()['data']['type'], womens['type']) 
        self.assertEqual(response.json()['data']['links'], womens['links']) 
        self.assertEqual(response.json()['data']['relationships'], womens['relationships'])         
        '''
        self.lg('%s ENDED' % self._testID)