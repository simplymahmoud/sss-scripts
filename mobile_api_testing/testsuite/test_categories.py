# -*- coding: utf-8 -*-
from testframework.base import *
import types


categories_response_headers = {'Transfer-Encoding': 'chunked', 
                               'Connection': 'keep-alive', 
                               'pragma': 'no-cache', 
                               'Cache-Control': 'private, must-revalidate', 
                               'Content-Type': 'application/vnd.api+json'}

womens = {
        "type": "categories",
        "id": "4",
        "attributes": {
            "parent_id": 2,
            "created_at": "2015-11-09 17:38:17",
            "updated_at": "2017-07-07 22:01:49",
            "position": 3,
            "level": 2,
            "children_count": 291,
            "name": "Womens",
            "slug": "womens",
            "description": "<p>Sun &amp; Sand Sports carries one of the greatest selections of activewear and sportswear for women.</p>",
            "screen_id": 33,
            "image_url": "https://sssports-media-res.cloudinary.com/w_936/media/catalog/category/CB_WOMENS_NIKE_PEGASUS_2017.jpg",
            "app_link": "sss://category/4"
        },
        "relationships": {
            "children": {
                "data": [
                    {
                        "type": "categories",
                        "id": "19"
                    },
                    {
                        "type": "categories",
                        "id": "29"
                    },
                    {
                        "type": "categories",
                        "id": "20"
                    },
                    {
                        "type": "categories",
                        "id": "53"
                    },
                    {
                        "type": "categories",
                        "id": "112"
                    },
                    {
                        "type": "categories",
                        "id": "896"
                    }
                ],
                "links": {
                    "self": "http://45.33.59.76/api/v1/categories/4/relationships/children",
                    "related": "http://45.33.59.76/api/v1/categories/4/children"
                }
            }
        },
        "links": {
            "self": "http://45.33.59.76/api/v1/categories/4"
        }
    }

no_categories = 15


class TestCategories(BaseTest):


    def test001_get_categories(self):
        """ TestCase-6: Test case for test get /categories.*
        **Test Scenario:**
        #. Get /categories, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/categories')
        
        self.lg('#. Get /categories, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        '''
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in categories_response_headers.keys()]
        [self.assertEqual(categories_response_headers[header], response.headers[header]) for header in categories_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.ListType)
        self.assertEqual(len(response.json()['data']), no_categories)
        [self.assertEqual(type(category_dict), types.DictType) for category_dict in response.json()['data']]

        for category_dict in response.json()['data']:
            for key in category_dict.keys():
                self.assertIn(key, womens.keys())
            if category_dict['id'] == womens['id']:
               self.assertEqual(category_dict['type'], womens['type']) 
               self.assertEqual(category_dict['links'], womens['links']) 
               self.assertEqual(category_dict['attributes'], womens['attributes']) 
               self.assertEqual(category_dict['relationships'], womens['relationships']) 
        '''
        self.lg('%s ENDED' % self._testID)                        
        

    def test002_get_category(self):
        """ TestCase-7: Test case for test get /categories/{id}.*
        **Test Scenario:**
        #. Get /categories/{id}, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_request_response(uri='/categories/%s' % womens['id'])
        
        self.lg('#. Get /categories/{id}, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        '''
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in categories_response_headers.keys()]
        [self.assertIn(categories_response_headers[header], response.headers[header]) for header in categories_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)
        self.assertEqual(response.json()['data']['id'], womens['id']) 
        self.assertEqual(response.json()['data']['type'], womens['type']) 
        self.assertEqual(response.json()['data']['links'], womens['links']) 
        self.assertEqual(response.json()['data']['attributes'], womens['attributes'])         
        '''
        self.lg('%s ENDED' % self._testID)