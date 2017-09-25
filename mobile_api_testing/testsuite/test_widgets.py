# -*- coding: utf-8 -*-
from testframework.base import *
import types


widgets_response_headers = {'Transfer-Encoding': 'chunked', 
                           'Connection': 'keep-alive', 
                           'pragma': 'no-cache', 
                           'Cache-Control': 'private, must-revalidate', 
                           'Content-Type': 'application/vnd.api+json'}

widgets = {"type":"widgets","id":"1","attributes":{"screen_id":1,"kind":"Category","index":2,"label":'',"dynamic":0,"text":'',"created_at":"2017-09-18 21:24:57","updated_at":"2017-09-18 21:24:57"},"relationships":{"blocks":{"data":[{"type":"blocks","id":"1"},{"type":"blocks","id":"2"},{"type":"blocks","id":"3"},{"type":"blocks","id":"4"}],"links":{"self":"https:\/\/api.sssports.com\/v1\/widgets\/1\/relationships\/blocks","related":"https:\/\/api.sssports.com\/v1\/widgets\/1\/blocks"}},"rules":{"data":[],"links":{"self":"https:\/\/api.sssports.com\/v1\/widgets\/1\/relationships\/rules","related":"https:\/\/api.sssports.com\/v1\/widgets\/1\/rules"}}},"links":{"self":"https:\/\/api.sssports.com\/v1\/widgets\/1"}}

no_widgets = 40


class TestWidgets(BaseTest):


    def test001_get_widgets(self):
        """ TestCase-14: Test case for test get /widgets.*
        **Test Scenario:**
        #. Get /widgets, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/widgets')
        
        self.lg('#. Get /widgets, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        '''
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in widgets_response_headers.keys()]
        [self.assertEqual(widgets_response_headers[header], response.headers[header]) for header in widgets_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.ListType)
        self.assertEqual(len(response.json()['data']), no_widgets)
        [self.assertEqual(type(widget_dict), types.DictType) for widget_dict in response.json()['data']]

        for widget_dict in response.json()['data']:
            for key in widget_dict.keys():
                self.assertIn(key, widgets.keys())
            if widget_dict['id'] == widgets['id']:
               self.assertEqual(widget_dict['type'], widgets['type']) 
               self.assertEqual(widget_dict['links'], widgets['links']) 
               #self.assertEqual(widget_dict['attributes'], widgets['attributes']) 
        '''
        self.lg('%s ENDED' % self._testID)                        
        

    def test002_get_widget(self):
        """ TestCase-15: Test case for test get /widgets/{id}.*
        **Test Scenario:**
        #. Get /widgets/{id}, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_request_response(uri='/widgets/%s' % widgets['id'])
        
        self.lg('#. Get /widgets/{id}, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        '''
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in widgets_response_headers.keys()]
        [self.assertIn(widgets_response_headers[header], response.headers[header]) for header in widgets_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)
        self.assertEqual(response.json()['data']['id'], widgets['id']) 
        self.assertEqual(response.json()['data']['type'], widgets['type']) 
        self.assertEqual(response.json()['data']['links'], widgets['links']) 
        #self.assertEqual(response.json()['data']['attributes'], widgets['attributes'])         
        '''
        self.lg('%s ENDED' % self._testID) 