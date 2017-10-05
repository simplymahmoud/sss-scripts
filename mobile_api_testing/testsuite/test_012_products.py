# -*- coding: utf-8 -*-
from testframework.base import *
import types


products_response_headers = {'Connection': 'Keep-Alive', 
                             'Cache-Control': 'public, s-maxage=86400', 
                             'Content-Type': 'application/vnd.api+json; charset=utf-8'}

products = {
        "type": "products",
        "id": "157414",
        "attributes": {
            "type_id": "configurable",
            "sku": "ADAP-AJ5843",
            "created_at": "2017-07-05 05:08:13",
            "updated_at": "2017-07-09 11:09:53",
            "price": 115,
            "final_price": 115,
            "parent_id": '',
            "name": "adidas Regista 16 Football Jersey",
            "slug": "adidas-regista-16-football-jersey-adap-aj5843",
            "thumbnail_url": "https://sssports-media-res.cloudinary.com/w_312/media/catalog/product/4/0/4055344451311_4.jpg",
            "quantity": 0,
            "is_available": False,
            "currency_code": "AED",
            "formatted_price": "115.00 AED",
            "formatted_final_price": "115.00 AED",
            "on_sale": False,
            "video_url": '',
            "description": "Take charge of the game with the adidas Regista 16 Football Jersey for men. Made for football, this jersey features a slim-fit design with mesh sleeves for maximum ventilation without compromising mobility. It’s not only breathable, but it also provides good coverage, cool contrasting diagonal stripe on the front and and the brand’s iconic 3-Stripe on the shoulders. \r\n\r\n<ul>\r\n<li>Slim fit</li>\r\n<li>Climacool® keeps you cool and dry</li>\r\n<li>Ribbed crewneck</li>\r\n<li>Mesh inserts for breathability</li>\r\n<li>Material composition: 100% Recycled polyester</li>\r\n</ul>",
            "selection_count": 2,
            "color_count": 1,
            "top_category_id": 131,
            "category_name": "Tops",
            "color_id": 13,
            "color": "Blue",
            "is_salable": False,
            "app_link": "sss://product/157414",
            "site_url": "https://sssports.com/adidas-regista-16-football-jersey-adap-aj5843",
            "image_url": "https://sssports-media-res.cloudinary.com/w_936/media/catalog/product/4/0/4055344451311_4.jpg"
        },
        "relationships": {
            "images": {
                "data": [
                    {
                        "type": "product-images",
                        "id": "1192692"
                    },
                    {
                        "type": "product-images",
                        "id": "1192693"
                    }
                ],
                "links": {
                    "self": "https://api-staging.sssports.com/v1/products/157414/relationships/images",
                    "related": "https://api-staging.sssports.com/v1/products/157414/images"
                }
            },
            "selections": {
                "data": [
                    {
                        "type": "selections",
                        "id": "29722"
                    },
                    {
                        "type": "selections",
                        "id": "29723"
                    }
                ],
                "links": {
                    "self": "https://api-staging.sssports.com/v1/products/157414/relationships/selections",
                    "related": "https://api-staging.sssports.com/v1/products/157414/selections"
                }
            },
            "children": {
                "data": [
                    {
                        "type": "product-children",
                        "id": "156875"
                    },
                    {
                        "type": "product-children",
                        "id": "156876"
                    },
                    {
                        "type": "product-children",
                        "id": "156877"
                    },
                    {
                        "type": "product-children",
                        "id": "156878"
                    },
                    {
                        "type": "product-children",
                        "id": "156879"
                    }
                ],
                "links": {
                    "self": "https://api-staging.sssports.com/v1/products/157414/relationships/children",
                    "related": "https://api-staging.sssports.com/v1/products/157414/children"
                }
            },
            "config": {
                "data": [],
                "links": {
                    "self": "https://api-staging.sssports.com/v1/products/157414/relationships/config",
                    "related": "https://api-staging.sssports.com/v1/products/157414/config"
                }
            }
        },
        "links": {
            "self": "/products/157414"
        }
    }

no_products = 1


class TestBrands(BaseTest):


    def test001_get_products(self):
        """ TestCase-20: Test case for test get /products.*
        **Test Scenario:**
        #. Get /products, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)
        response = self.get_request_response(uri='/products?filter%5Btype_id%5D=configurable&page%5Bsize%5D=1&filter%5Bhas_options%5D=1')
        
        self.lg('#. Get /products, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in products_response_headers.keys()]
        [self.assertEqual(products_response_headers[header], response.headers[header]) for header in products_response_headers.keys()]
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)
        '''
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.ListType)
        self.assertEqual(len(response.json()['data']), no_products)
        [self.assertEqual(type(product_dict), types.DictType) for product_dict in response.json()['data']]

        for product_dict in response.json()['data']:
            for key in product_dict.keys():
                self.assertIn(key, products.keys())
            if product_dict['id'] == products['id']:
               self.assertEqual(product_dict['type'], products['type']) 
               self.assertEqual(product_dict['links'], products['links']) 
               #self.assertEqual(product_dict['attributes'], products['attributes']) 
        '''
        self.lg('%s ENDED' % self._testID)                        
        

    def test002_get_product(self):
        """ TestCase-21: Test case for test get /products/{id}.*
        **Test Scenario:**
        #. Get /products/{id}, should succeed
        #. Check response headers, should succeed
        #. Check response body, should succeed
        """    	
        self.lg('%s STARTED' % self._testID)   
        response = self.get_request_response(uri='/products/%s' % products['id'])
        
        self.lg('#. Get /products/{id}, should succeed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)        
        
        self.lg('#. Check response headers, should succeed')
        [self.assertIn(header, response.headers.keys()) for header in products_response_headers.keys()]
        [self.assertEqual(products_response_headers[header], response.headers[header]) for header in products_response_headers.keys()]        
        
        self.lg('#. Check response body, should succeed')
        self.assertEqual(type(response.json()), types.DictType)  
        '''
        self.assertIn('data', response.json().keys())
        self.assertEqual(type(response.json()['data']), types.DictType)
        self.assertEqual(response.json()['data']['id'], products['id']) 
        self.assertEqual(response.json()['data']['type'], products['type']) 
        self.assertEqual(response.json()['data']['links'], products['links']) 
        #self.assertEqual(response.json()['data']['attributes'], products['attributes'])         
        '''
        self.lg('%s ENDED' % self._testID) 