# -*- coding: utf-8 -*-
from testframework.base import *
import types


screens_response_headers = {'Connection': 'Keep-Alive', 
                            'Cache-Control': 'public, s-maxage=86400', 
                            'Content-Type': 'application/vnd.api+json; charset=utf-8'}

screens = {"type":"screens","id":"1","attributes":{"title":"Homepage Iteration 1 (EN)","kind":"home","status":1,"created_at":'',"updated_at":''},"relationships":{"widgets":{"data":[{"type":"widgets","id":"1"},{"type":"widgets","id":"2"},{"type":"widgets","id":"3"},{"type":"widgets","id":"4"}],"links":{"self":"https:\/\/api.sssports.com\/v1\/screens\/1\/relationships\/widgets","related":"https:\/\/api.sssports.com\/v1\/screens\/1\/widgets"}}},"links":{"self":"https:\/\/api.sssports.com\/v1\/screens\/1"}}

no_screens = 6


class TestScreens(BaseTest):


    def test001_get_screens(self):
        """ TestCase-25: Test case for test get /screens.*
        **Test Scenario:**
        #. Get /screens, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/screens')
        
        self.lg('#. Get /screens, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in screens_response_headers.keys()]
        [self.assertEqual(screens_response_headers[header], response.headers[header]) for header in screens_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)
        '''
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.ListType)
        self.assertEqual(len(response.json()['data']), no_screens)
        [self.assertEqual(type(screen_dict), types.DictType) for screen_dict in response.json()['data']]

        for screen_dict in response.json()['data']:
            for key in screen_dict.keys():
                self.assertIn(key, screens.keys())
            if screen_dict['id'] == screens['id']:
               self.assertEqual(screen_dict['type'], screens['type']) 
               self.assertEqual(screen_dict['links'], screens['links']) 
               #self.assertEqual(screen_dict['attributes'], screens['attributes']) 
        '''
        self.lg('%s ENDED' % self._testID)                        
        

    def test002_get_screen(self):
        """ TestCase-26: Test case for test get /screens/{id}.*
        **Test Scenario:**
        #. Get /screens/{id}, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_request_response(uri='/screens/%s' % screens['id'])
        
        self.lg('#. Get /screens/{id}, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in screens_response_headers.keys()]
        [self.assertEqual(screens_response_headers[header], response.headers[header]) for header in screens_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        '''
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)
        self.assertEqual(response.json()['data']['id'], screens['id']) 
        self.assertEqual(response.json()['data']['type'], screens['type']) 
        self.assertEqual(response.json()['data']['links'], screens['links']) 
        #self.assertEqual(response.json()['data']['attributes'], screens['attributes'])         
        '''
        self.lg('%s ENDED' % self._testID) 