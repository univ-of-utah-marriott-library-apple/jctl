#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JSS api
"""

import logging
import requests
import json
import pprint

from . import cache

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"


class Error(Exception):
    pass


class APIError(Error):
    pass


class TestError(Error):
    def __init__(self, response, *args):
        Error.__init__(self, *args)
        self.code = response.status_code
        self.url = response.url


class JSS(object):
    """
    Class for making api calls to JSS
    """
    def __init__(self, address, auth=()):
        self.log = logging.getLogger(f"{__name__}.JSS")
        self.url = f"https://{address}:8443/JSSResource"
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json',
                                     'Content-Type': 'application/xml'})
        if auth:
            # auth must be a tuple
            self.session.auth = tuple(auth)
        
    def get(self, endpoint):        
        """
        :param endpoint:    URI of api call (e.g. "policies/id/1")
        :returns dict:      response data
        """
        url = f"{self.url}/{endpoint}"
        self.log.info(f"getting: {endpoint!r}")                
        response = self.session.get(url)
        # self.log.debug(f"RESPONSE: {dump_object(response)}")
        if response.status_code != 200:
            err = f"GET failed: {response.status_code} {url}\n{response.text}"
            self.log.error(err)
            raise APIError(err)
        # return response.text
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            self.log.error(f"invalid JSON: {response.text}")
            raise
    
    def post(self, endpoint, data):
        url = f"{self.url}/{endpoint}"
        self.log.info(f"creating: {endpoint!r}")
        response = self.session.post(url, data=xml_from_dict(data))
        if response.status_code != 201:
            err = f"POST failed: {response.status_code} {url}\n{response.text}"
            self.log.error(err)
            raise APIError(err)
    
    def put(self, endpoint, data):
        url = f"{self.url}/{endpoint}"
        self.log.info(f"updating: {endpoint!r}")
        response = self.session.put(url, data=xml_from_dict(data))
        if response.status_code != 201:
            err = f"PUT failed: {response.status_code} {url}\n{response.text}"
            self.log.error(err)
            raise APIError(err)
            raise APIError(f"PUT failed: {response.text}")
    
    def __del__(self):
        self.log.debug("closing session")
        self.session.close()


# class MutableJSSObject(object):
#     
#     def __init__(self, key, value):
#         self._key = key
#         self._value = value
#     
#     def __setattr__(self):
#         pass


class JSSObject(object):
    
    def __init__(self, data):
        self._data = data
        self._id = data['id']
        self._name = data['name']
        self._modified = False
    
    @property
    def jssid(self):
        return self._id
    
    @property
    def modified(self):
        return self._modified
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, string):
        self._modified = True
        self._name = string

    @property
    def xml(self):
        return xml_from_dict(self._data)


def xml_from_dict(data):
    """
    converts python dict to xml string
    """
    if isinstance(data, dict):
        xml_str = ''
        for key, value in data.items():
            result = xml_from_dict(value)
            xml_str += f"<{key}>{result}</{key}>"
    elif isinstance(data, list):
        xml_str = xml_from_dict(value)
    else:
        xml_str = f"{data}"
    
    return xml_str
      

def dump_object(obj):
    _data = {}
    for k in dir(obj):
        _data[k] = getattr(obj, k)
    return _data



if __name__ == '__main__':
    pass