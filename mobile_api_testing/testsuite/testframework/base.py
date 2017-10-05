# -*- coding: utf-8 -*-
import logging
import time
import os

from testconfig import config
from unittest import TestCase
import requests


class BaseTest(TestCase):


    logger = logging.getLogger('api_testsuite')
    if not os.path.exists('logs/api_testsuite.log'):os.mkdir('logs')
    handler = logging.FileHandler('logs/api_testsuite.log')
    formatter = logging.Formatter('%(asctime)s [%(testid)s] [%(levelname)s] %(message)s',
                                  '%d/%m/%Y %I:%M:%S %p')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        self.environment_url = config['main']['url']
        self.client_auth_header = {}
        for cfg in config['client_token'].keys():
            self.client_auth_header[cfg] = config['client_token'][cfg]
        self.user_auth_header = {}
        for cfg in config['user_token'].keys():
            self.user_auth_header[cfg] = config['user_token'][cfg]     
        self.use_auth = config['main']['use_auth']


    def setUp(self):
        self._testID = self._testMethodName
        self.url = self.environment_url + '/v1'
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('api_testsuite'),
                                             {'testid': self.shortDescription().split(':')[0] or self._testID})
        self.lg('Testcase %s Started at %s' % (self._testID, self._startTime))
        self.session = requests.Session()
        if self.use_auth == 'True':
            self.add_bearer_auth_to_header()


    def tearDown(self):
        """
        Environment cleanup and logs collection.
        """
        self.session.close()
        if hasattr(self, '_startTime'):
            executionTime = time.time() - self._startTime
        self.lg('Testcase %s Execution Time is %s sec.' % (self._testID, executionTime))


    def lg(self, msg):
        self._logger.info(msg)
        
        
    def get_request_response(self, uri, headers=None, payload=None):
        if headers == None: 
            headers = {"Content-Type": "application/vnd.api+json"}
        if hasattr(self, 'auth_header'):
            headers['Authorization'] = self.auth_header
        self.lg('GET %s' % self.url + uri)
        return self.session.get(self.url + uri, params=payload, headers=headers, timeout=30, allow_redirects=False)     


    def post_request_response(self, uri, data, headers=None):  
        if headers == None: 
            headers = {"Content-Type": "application/vnd.api+json"}
        if hasattr(self, 'auth_header'):
            headers['Authorization'] = self.auth_header         
        self.lg('POST %s' % self.url + uri)
        return self.session.post(self.url + uri, data=data, headers=headers, timeout=30, allow_redirects=False)        


    def delete_request_response(self, uri, headers=None):      
        if headers == None: 
            headers = {"Content-Type": "application/vnd.api+json"}
        if hasattr(self, 'auth_header'):
            headers['Authorization'] = self.auth_header
        self.lg('DELETE %s' % self.url + uri)
        return self.session.delete(self.url + uri, headers=headers, timeout=30, allow_redirects=False)
    
    
    def get_token_response(self, data):
        self.lg('GET TOKEN RESONSE with DATA: %s' % data)
        return self.session.post(self.environment_url + '/oauth/token', data=data)    
    
    
    def add_bearer_auth_to_header(self):
        response = self.get_token_response(self.client_auth_header)
        self.auth_header = response.json()['token_type'] + ' ' + response.json()['access_token']    
        self.lg('ADD BEARER AUTH to HEADER: %s' % self.auth_header)


    def get_sli_search(self, keyword):
        self.lg('GET SLI SEARCH for KEWORD: %s' % keyword)
        return self.session.get('https://shop.sssports.com/search?w=%s&ts=json-full' % keyword, timeout=30, allow_redirects=False)