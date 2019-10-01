#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JSS api
"""

import logging
import requests
import json
import pprint
import os
import subprocess

from . import cache
from . import convert

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"


class Error(Exception):
    pass


class APIError(Error):
    pass


class JSS(object):
    """
    Class for making api calls to JSS
    """
    def __init__(self, address, auth=()):
        self.log = logging.getLogger(f"{__name__}.JSS")
        self.url = f"https://{address}:8443/JSSResource"
        self.session = requests.Session()
        if auth:
            # auth must be a tuple
            self.session.auth = tuple(auth)
        
    def get(self, endpoint, xml=False):        
        """
        :param endpoint:    URI of api call (e.g. "policies/id/1")
        :returns dict:      response data
        """
        url = f"{self.url}/{endpoint}"
        self.log.debug(f"getting: {endpoint!r}")
        headers = {'Accept': 'application/xml'} if xml else {}
        response = self.session.get(url, headers=headers)

        if response.status_code != 200:
            raise APIError(f"{url}: {response}")
        
        if xml:
            return convert.xml_to_dict(response.text)
        else:
            return response.json()
    
    def post(self, endpoint, data):
        url = f"{self.url}/{endpoint}"
        self.log.info(f"creating: {endpoint!r}")
        response = self.session.post(url, data=convert.dict_to_xml(data))
        if response.status_code != 201:
            err = f"POST failed: {response.status_code} {url}\n{response.text}"
            self.log.error(err)
            raise APIError(err)
        return convert.xml_to_dict(response.text)
    
    def put(self, endpoint, data):
        url = f"{self.url}/{endpoint}"
        self.log.info(f"updating: {endpoint!r}")
        response = self.session.put(url, data=convert.dict_to_xml(data))
        if response.status_code != 201:
            err = f"PUT failed: {response.status_code} {url}"
            self.log.error(err)
            self.log.debug(f"HEADERS: {response.headers}")
            self.log.debug(f"   TEXT: {response.text}")
            raise APIError(err)
            
    def upload(self, endpoint, path, name=None, mime_type=None):
        url = f"{self.url}/fileuploads/{endpoint}"
        self.log.debug(f"uploading: {url!r}: {path!r}")
        
        if not mime_type:
            # determine mime-type of file if not specified
            mime_type = mime_type(path)

        if not name:
            name = os.path.basename(path)  
        elif not os.path.splitext(name)[1]:
            # get extension from mime-type
            ext = mime_type.split('/')[1]
            # upload will fail if w/o extension
            name = f"{name}.{ext}"

        with open(path, 'rb') as f:
            ## example of posted file data:
            # {'name': ('example.png', 
            #           <_io.BufferedReader name="./example.png">,
            #           'image/png')}
            files = {'name': (name, f, mime_type)}
            self.log.debug(f"files: {files}")
            response = self.session.post(url, files=files)

        if response.status_code != 201:
            err = f"PUT failed: {response.status_code} {url}"
            self.log.error(err)
            self.log.debug(f"RESPONSE: headers: {response.headers}")
            self.log.debug(f"   TEXT: {response.text}")
            raise APIError(err)
        
    def __del__(self):
        self.log.debug("closing session")
        self.session.close()


def mime_type(path):
    """
    returns content type of file
    uses `/usr/bin/file` to determine mime-type of file
    """
    cmd = ['/usr/bin/file', '-b', '--mime-type', path]
    return subprocess.check_output(cmd).rstrip()


# class MutableJSSObject(object):
#     
#     def __init__(self, key, value):
#         self._key = key
#         self._value = value
#     
#     def __setattr__(self):
#         pass


# class JSSObject(object):
#     
#     def __init__(self, data):
#         self._data = data
#         self._id = data['id']
#         self._name = data['name']
#         self._modified = False
#     
#     @property
#     def jssid(self):
#         return self._id
#     
#     @property
#     def modified(self):
#         return self._modified
#     
#     @property
#     def name(self):
#         return self._name
#     
#     @name.setter
#     def name(self, string):
#         self._modified = True
#         self._name = string
# 
#     @property
#     def xml(self):
#         return xml_from_dict(self._data)


# def xml_from_dict(data):
#     """
#     converts python dict to xml string
#     """
#     if isinstance(data, dict):
#         xml_str = ''
#         for key, value in data.items():
#             result = xml_from_dict(value)
#             xml_str += f"<{key}>{result}</{key}>"
#     elif isinstance(data, list):
#         xml_str = xml_from_dict(value)
#     else:
#         xml_str = f"{data}"
#     
#     return xml_str
      

# def dump_object(obj):
#     _data = {}
#     for k in dir(obj):
#         _data[k] = getattr(obj, k)
#     return _data
# 


if __name__ == '__main__':
    pass
