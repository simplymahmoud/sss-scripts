# -*- coding: utf-8 -*-
from testframework.base import *
import types


menu_items_response_headers = {'Connection': 'Keep-Alive', 
                          'Cache-Control': 'public, s-maxage=86400', 
                          'Content-Type': 'application/vnd.api+json; charset=utf-8'}

menu_items = {
            "type": "menu-items",
            "id": "1",
            "attributes": {
                "menu_id": 1,
                "menu_item_id": None,
                "category_id": 125,
                "position": 0,
                "title": "Mens",
                "link": "sss://plp/125",
                "created_at": "2017-10-01 23:34:41",
                "updated_at": "2017-10-01 23:34:41"
            },
            "relationships": {
                "children": {
                    "data": [
                        {
                            "type": "menu-items",
                            "id": "2"
                        },
                        {
                            "type": "menu-items",
                            "id": "13"
                        },
                        {
                            "type": "menu-items",
                            "id": "21"
                        },
                        {
                            "type": "menu-items",
                            "id": "28"
                        },
                        {
                            "type": "menu-items",
                            "id": "38"
                        },
                        {
                            "type": "menu-items",
                            "id": "47"
                        }
                    ],
                    "links": {
                        "self": "https://api-staging.sssports.com/v1/menu-items/1/relationships/children",
                        "related": "https://api-staging.sssports.com/v1/menu-items/1/children"
                    }
                },
                "menu": {
                    "data": {
                        "type": "menu",
                        "id": "1"
                    },
                    "links": {
                        "self": "https://api-staging.sssports.com/v1/menu-items/1/relationships/menu",
                        "related": "https://api-staging.sssports.com/v1/menu-items/1/menu"
                    }
                }
            },
            "links": {
                "self": "https://api-staging.sssports.com/v1/menu-items/1"
            }
        }

no_menu_items = 296


class TestMenuItems(BaseTest):


    def test001_get_menu_items(self):
        """ TestCase-15: Test case for test get /menu-items.*
        **Test Scenario:**
        #. Get /menu-items, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/menu-items')
        
        self.lg('#. Get /menu-items, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in menu_items_response_headers.keys()]
        [self.assertEqual(menu_items_response_headers[header], response.headers[header]) for header in menu_items_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)

        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.ListType)
        self.assertEqual(len(response.json()['data']), no_menu_items)
        [self.assertEqual(type(file_dict), types.DictType) for file_dict in response.json()['data']]

        for category_dict in response.json()['data']:
            for key in category_dict.keys():
                self.assertIn(key, menu_items.keys())
            if file_dict['id'] == menu_items['id']:
               self.assertEqual(file_dict['type'], menu_items['type']) 
               self.assertEqual(file_dict['links'], menu_items['links']) 
               self.assertEqual(file_dict['attributes'], menu_items['attributes']) 

        self.lg('%s ENDED' % self._testID)                        
        

    def test002_get_menu(self):
        """ TestCase-16: Test case for test get /menu-items/{id}.*
        **Test Scenario:**
        #. Get /menu-items/{id}, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_request_response(uri='/menu-items/%s' % menu_items['id'])
        
        self.lg('#. Get /menu-items/{id}, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in menu_items_response_headers.keys()]
        [self.assertIn(menu_items_response_headers[header], response.headers[header]) for header in menu_items_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)
        self.assertEqual(response.json()['data']['id'], menu_items['id']) 
        self.assertEqual(response.json()['data']['type'], menu_items['type']) 
        self.assertEqual(response.json()['data']['links'], menu_items['links']) 
        self.assertEqual(response.json()['data']['attributes'], menu_items['attributes'])         

        self.lg('%s ENDED' % self._testID)