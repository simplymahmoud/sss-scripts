# -*- coding: utf-8 -*-
from testframework.base import *
import types


brands_response_headers = {'Connection': 'Keep-Alive', 
                           'Cache-Control': 'public, s-maxage=86400', 
                           'Content-Type': 'application/vnd.api+json; charset=utf-8'}

adidas = {"type": "brands",
          "id": "1",
          "attributes": {"name": "adidas",
                         "slug": "adidas",
                         "thumbnail_image": "https://images-cdn.sssports.com/brands/NAV-BAR_BRANDS_ADIDAS_001_28122015_2.png",
                         "featured": 1},
          "links": {"self": "http://45.33.59.76/api/v1/brands/1"}}

no_brands = 113


class TestBrands(BaseTest):


    def test001_get_brands(self):
        """ TestCase-6: Test case for test get /brands.*
        **Test Scenario:**
        #. Get /brands, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/brands')
        
        self.lg('#. Get /brands, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in brands_response_headers.keys()]
        [self.assertEqual(brands_response_headers[header], response.headers[header]) for header in brands_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)
        
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.ListType)
        '''
        self.assertEqual(len(response.json()['data']), no_brands)
        [self.assertEqual(type(brand_dict), types.DictType) for brand_dict in response.json()['data']]

        for brand_dict in response.json()['data']:
            for key in brand_dict.keys():
                self.assertIn(key, adidas.keys())
            if brand_dict['id'] == adidas['id']:
               self.assertEqual(brand_dict['type'], adidas['type']) 
               self.assertEqual(brand_dict['links'], adidas['links']) 
               self.assertEqual(brand_dict['attributes'], adidas['attributes']) 
        '''
        self.lg('%s ENDED' % self._testID)                        
        

    def test002_get_brand(self):
        """ TestCase-7: Test case for test get /brands/{id}.*
        **Test Scenario:**
        #. Get /brands/{id}, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_request_response(uri='/brands/%s' % adidas['id'])
        
        self.lg('#. Get /brands/{id}, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in brands_response_headers.keys()]
        [self.assertIn(brands_response_headers[header], response.headers[header]) for header in brands_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)
        '''
        self.assertEqual(response.json()['data']['id'], adidas['id']) 
        self.assertEqual(response.json()['data']['type'], adidas['type']) 
        self.assertEqual(response.json()['data']['links'], adidas['links']) 
        self.assertEqual(response.json()['data']['attributes'], adidas['attributes'])         
        '''
        self.lg('%s ENDED' % self._testID) 