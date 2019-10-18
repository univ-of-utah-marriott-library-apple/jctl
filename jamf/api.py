# -*- coding: utf-8 -*-

"""
JSS API
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.2.1"

import logging
import requests
import os
import subprocess
import plistlib

# from . import cache
from . import convert


class Error(Exception):
    pass


class APIError(Error):
    def __init__(self, response, msg):
        self.response = response
        self.status_code = response.status_code
        self.message = msg


class API(object):
    """
    Class for making api calls to JSS
    """

    def __init__(self, address=None, auth=(), config=None):
        """
        Create requests.Session with JSS address and authentication

        :param address <str>:   JSS address (e.g. 'your.jss.domain')
        :param auth <tuple>:    JSS authentication credentials (user, passwd)
        """
        self.log = logging.getLogger(f"{__name__}.JSS")
        if config:
            address, auth = apiconfig(config)
        if not address:
            raise Error("no address specified")
        self.url = f"https://{address}:8443/JSSResource"
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/xml'})
        if auth:
            self.session.auth = tuple(auth)
        
    def get(self, endpoint, json=False, raw=False):        
        """
        Get JSS information
        
        :param endpoint <str>:  API endpoint (e.g. "policies/id/1")
        :param json <bool>:     request JSON response (sometimes incomplete)
        :param raw  <bool>:     return requests.Response obj (skip errors)

        :returns dict||requests.Resonse obj:
        """
        url = f"{self.url}/{endpoint}"
        self.log.debug(f"endpoint: {endpoint!r}")

        # modify headers for JSON (if applicable)
        headers = {'Accept': 'application/json'} if json else {}
        response = self.session.get(url, headers=headers)
        
        # return raw requests.Response object before Exception can be raised
        if raw:
            return response

        # raise Exception if GET failed
        if response.status_code != 200:
            # TO-DO: convert a response to an actual error message
            err = f"GET failed: {url}: {response}"
            self.log.error(err)
            self.log.debug(f"TEXT: {response.text}")
            raise APIError(response, err)
        
        # convert response.text based on specified format
        if json:
            # convert json response.text
            return response.json()
        else:
            # convert xml response.text
            return convert.xml_to_dict(response.text)
                            
    def post(self, endpoint, data, raw=False):
        """
        Create new entries on JSS

        :param endpoint <str>:  JSS endpoint (e.g. "policies/id/0")
        :param data <dict>:     data to be submitted

        :returns dict:          response data
        """
        url = f"{self.url}/{endpoint}"
        self.log.info(f"creating: {endpoint!r}")
        response = self.session.post(url, data=convert.dict_to_xml(data))

        # return raw requests.Response object before Exception can be raised
        if raw:
            return response

        # raise Exception if POST failed
        if response.status_code != 201:
            err = f"POST failed: {url}: {response}"
            self.log.error(err)
            self.log.debug(f"TEXT: {response.text}")
            raise APIError(response, err)

        # return succesful response data (usually {'id': jssid})
        return convert.xml_to_dict(response.text)
    
    def put(self, endpoint, data, raw=False):
        """
        Update existing entries on JSS

        :param endpoint <str>:  JSS endpoint (e.g. "policies/id/0")
        :param data <dict>:     data to be submitted

        :returns dict:          response data
        """
        url = f"{self.url}/{endpoint}"
        self.log.info(f"updating: {endpoint!r}")
        response = self.session.put(url, data=convert.dict_to_xml(data))
        
        # return raw requests.Response object before Exception can be raised
        if raw:
            return response
        
        # raise Exception if PUT failed
        if response.status_code != 201:
            err = f"PUT failed: {url}: {response}"
            self.log.error(err)
            self.log.debug(f"TEXT: {response.text}")
            raise APIError(response, err)

        # return succesful response data (usually {'id': jssid})
        return convert.xml_to_dict(response.text)
            
    def upload(self, endpoint, path, name=None, mime_type=None):
        """
        Upload files to JSS

        :param endpoint <str>:   JSS fileuploads endpoint (e.g. "policies/id/0")
        :param path <str>:       Path to file

        Optional:
        :param name <str>:       Name of file (requires extension)
        :param mime_type <str>:  MIME type (e.g. 'image/png')
        
        MIME type will attempt to be calculated via `file` if unspecified
        if extension is missing, it will be assumed via 

        :returns None:
        """
        url = f"{self.url}/fileuploads/{endpoint}"
        self.log.debug(f"uploading: {url!r}: {path!r}")
        
        # determine filename (if unspecified)
        if not name:
            name = os.path.basename(path)  

        # NOTE: JSS requires filename extension (or upload will fail)
        if not os.path.splitext(name)[1]:
            raise APIError(response, f"missing file extension: {path!r}")

        # determine mime-type of file (if unspecified)
        if not mime_type:
            mime_type = mime_type(path)

        with open(path, 'rb') as f:
            # Example of posted data:
            # {'name': ('example.png', 
            #           <_io.BufferedReader name="./example.png">,
            #           'image/png')}
            files = {'name': (name, f, mime_type)}
            self.log.debug(f"files: {files}")
            response = self.session.post(url, files=files)

        if response.status_code != 201:
            err = f"PUT failed: {url}: {response}"
            self.log.error(err)
            self.log.debug(f"TEXT: {response.text}")
            raise APIError(response, err)
        
    def __del__(self):
        self.log.debug("closing session")
        self.session.close()


def mime_type(path):
    """
    Uses `/usr/bin/file` to determine mime-type (requires Developer Tools)
    
    :param path <str>:  Path to file
    :returns str:       content type of file
    """
    cmd = ['/usr/bin/file', '-b', '--mime-type', path]
    return subprocess.check_output(cmd).rstrip()


def apiconfig(plist):
    """
    loads configuration from plist
    :returns: address, (username, passwd)
    """
    with open(plist, 'rb') as f:
        c = plistlib.load(f)
    user, passwd = c['login'].split(':')
    return c['address'], (user, passwd)


if __name__ == '__main__':
    pass
