# -*- coding: utf-8 -*-
from testframework.base import *
import types


regions_response_headers = {'Connection': 'Keep-Alive', 
                            'Cache-Control': 'public, s-maxage=86400', 
                            'Content-Type': 'application/vnd.api+json; charset=utf-8'}

regions = {
            "type": "regions",
            "id": "1",
            "attributes": {
                "country_id": 1,
                "name": "Badakhshan",
                "code": "BDS"
            },
            "links": {
                "self": "https://api-staging.sssports.com/v1/regions/1"
            }
        }

no_regions = 4332



class TestRegions(BaseTest):


    def test001_get_regions(self):
        """ TestCase-22: Test case for test get /regions.*
        **Test Scenario:**
        #. Get /regions, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/regions')
        
        self.lg('#. Get /regions, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in regions_response_headers.keys()]
        [self.assertEqual(regions_response_headers[header], response.headers[header]) for header in regions_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)

        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.ListType)
        self.assertEqual(len(response.json()['data']), no_regions)
        [self.assertEqual(type(regions_dict), types.DictType) for regions_dict in response.json()['data']]

        for regions_dict in response.json()['data']:
            for key in regions_dict.keys():
                self.assertIn(key, regions.keys())
            if regions_dict['id'] == regions['id']:
               self.assertEqual(regions_dict['type'], regions['type']) 
               self.assertEqual(regions_dict['links'], regions['links']) 

        self.lg('%s ENDED' % self._testID)                        