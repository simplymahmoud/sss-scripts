# -*- coding: utf-8 -*-
from testframework.base import *
import types


menus_response_headers = {'Connection': 'Keep-Alive', 
                          'Cache-Control': 'public, s-maxage=86400', 
                          'Content-Type': 'application/vnd.api+json; charset=utf-8'}

menus = {
            "type": "menu",
            "id": "1",
            "attributes": {
                "title": "Main Menu (GB)",
                "created_at": None,
                "updated_at": None
            },
            "relationships": {
                "menu-items": {
                    "data": None,
                    "links": {
                        "self": "https://api-staging.sssports.com/v1/menu/1/relationships/menu-items",
                        "related": "https://api-staging.sssports.com/v1/menu/1/menu-items"
                    }
                },
                "stores": {
                    "data": [
                        {
                            "type": "stores",
                            "id": "1"
                        },
                        {
                            "type": "stores",
                            "id": "8"
                        },
                        {
                            "type": "stores",
                            "id": "9"
                        },
                        {
                            "type": "stores",
                            "id": "10"
                        },
                        {
                            "type": "stores",
                            "id": "11"
                        },
                        {
                            "type": "stores",
                            "id": "12"
                        },
                        {
                            "type": "stores",
                            "id": "13"
                        }
                    ],
                    "links": {
                        "self": "https://api-staging.sssports.com/v1/menu/1/relationships/stores",
                        "related": "https://api-staging.sssports.com/v1/menu/1/stores"
                    }
                }
            },
            "links": {
                "self": "https://api-staging.sssports.com/v1/menu/1"
            }
        }

no_menus = 1


class TestMenus(BaseTest):


    def test001_get_menus(self):
        """ TestCase-17: Test case for test get /menus.*
        **Test Scenario:**
        #. Get /menus, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/menus')
        
        self.lg('#. Get /menus, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in menus_response_headers.keys()]
        [self.assertEqual(menus_response_headers[header], response.headers[header]) for header in menus_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)

        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.ListType)
        self.assertEqual(len(response.json()['data']), no_menus)
        [self.assertEqual(type(file_dict), types.DictType) for file_dict in response.json()['data']]

        for category_dict in response.json()['data']:
            for key in category_dict.keys():
                self.assertIn(key, menus.keys())
            if file_dict['id'] == menus['id']:
               self.assertEqual(file_dict['type'], menus['type']) 
               self.assertEqual(file_dict['links'], menus['links']) 
               self.assertEqual(file_dict['attributes'], menus['attributes']) 

        self.lg('%s ENDED' % self._testID)                        
        

    def test002_get_menu(self):
        """ TestCase-18: Test case for test get /menus/{id}.*
        **Test Scenario:**
        #. Get /menus/{id}, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_request_response(uri='/menus/%s' % menus['id'])
        
        self.lg('#. Get /menus/{id}, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in menus_response_headers.keys()]
        [self.assertIn(menus_response_headers[header], response.headers[header]) for header in menus_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)
        self.assertEqual(response.json()['data']['id'], menus['id']) 
        self.assertEqual(response.json()['data']['type'], menus['type']) 
        self.assertEqual(response.json()['data']['links'], menus['links']) 
        self.assertEqual(response.json()['data']['attributes'], menus['attributes'])         

        self.lg('%s ENDED' % self._testID)