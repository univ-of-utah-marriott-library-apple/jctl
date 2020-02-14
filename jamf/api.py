# -*- coding: utf-8 -*-

"""
JSS API
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2020 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.3.0"

import logging
import pathlib
import requests
import plistlib
import subprocess
import html.parser

try:
    from bs4 import BeautifulSoup
except ImportError:
    # will rely on JSSErrorParser
    pass

# local imports
from . import convert
from . import config


class Error(Exception):
    pass


class APIError(Error):

    def __init__(self, response):
        self.response = response
        err = parse_html_error(response.text)
        self.message = ": ".join(err) or 'failed'

    def __getattr__(self, attr):
        """
        missing attributes fallback on response
        """
        return getattr(self.response, attr)

    def __str__(self):
        r = self.response
        return f"{r}: {r.request.method} - {r.url}: {self.message}"


class Singleton(type):
    _instances = {}
    def __call__(cls, *a, **kw):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*a, **kw)
        return cls._instances[cls]


class API(metaclass=Singleton):
    """
    Class for making api calls to JSS
    """

    def __init__(self, hostname=None, auth=(), path=None):
        """
        Create requests.Session with JSS address and authentication

        :param address <str>:   JSS address (e.g. 'your.jss.domain')
        :param auth <tuple>:    JSS authentication credentials (user, passwd)
        """
        self.log = logging.getLogger(f"{__name__}.API")
        conf = config.SecureConfig(path=path)
        # get url from /Library/Preferences/com.jamfsoftware.jamf.plist?
        hostname = hostname or conf.get('JSSHostname', prompt='JSS Hostname')
        self.url = f"https://{hostname}:8443/JSSResource"
        self.session = requests.Session()
        self.session.auth = conf.credentials(hostname, auth)
        self.session.headers.update({'Accept': 'application/xml'})

    def get(self, endpoint, json=False, raw=False):
        """
        Get JSS information

        :param endpoint <str>:  API endpoint (e.g. "policies/id/1")
        :param json <bool>:     request JSON response (sometimes incomplete)
        :param raw  <bool>:     return requests.Response obj (skip errors)

        :returns <dict|requests.Response>:
        """
        url = f"{self.url}/{endpoint}"
        self.log.debug(f"getting: {endpoint!r}")

        # modify headers for JSON (if applicable)
        headers = {'Accept': 'application/json'} if json else {}
        response = self.session.get(url, headers=headers)

        if not response.ok:
            # return raw response before Exception is raised
            if raw:
                return response
            raise APIError(response)

        # return json or converted XML
        return response.json() if json else convert.xml_to_dict(response.text)

    def post(self, endpoint, data, raw=False):
        """
        Create new entries on JSS

        :param endpoint <str>:  JSS endpoint (e.g. "policies/id/0")
        :param data <dict>:     data to be submitted

        :returns dict:          response data
        """
        url = f"{self.url}/{endpoint}"
        self.log.debug(f"creating: {endpoint!r}")
        if isinstance(data, dict):
            data = convert.dict_to_xml(data)
        response = self.session.post(url, data=data)

        if not response.ok:
            # return raw response before Exception is raised
            if raw:
                return response
            raise APIError(response)

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
        self.log.debug(f"updating: {endpoint!r}")
        if isinstance(data, dict):
            data = convert.dict_to_xml(data)
        response = self.session.put(url, data=data)

        if not response.ok:
            # return raw response before Exception is raised
            if raw:
                return response
            raise APIError(response)

        # return succesful response data (usually: {'id': jssid})
        return convert.xml_to_dict(response.text)

    def upload(self, endpoint, path, name=None, mime_type=None):
        """
        Upload files to JSS

        :param endpoint <str>:   JSS fileuploads endpoint (e.g. "policies/id/0")
        :param path <str>:       Path to file

        Optional:
        :param name <str>:       Name of file (requires extension)
        :param mime_type <str>:  MIME type (e.g. 'image/png')

        if unspecified, MIME type will attempt to be calculated via `file`

        :returns None:
        """
        url = f"{self.url}/fileuploads/{endpoint}"
        path = pathlib.Path(path)
        self.log.debug(f"uploading: {url!r}: {path}")

        if not path.exists():
            raise FileNotFoundError(path)
        # determine filename (if unspecified)
        name = name or path.name()

        # NOTE: JSS requires filename extension (or upload will fail)
        if not path.suffix:
            raise Error(f"missing file extension: {path}")

        # determine mime-type of file (if unspecified)
        mime_type = mime_type or file_mime_type(path)

        with open(path, 'rb') as f:
            # Example of posted data:
            # {'name': ('example.png',
            #           <_io.BufferedReader name="./example.png">,
            #           'image/png')}
            files = {'name': (name, f, mime_type)}
            self.log.debug(f"files: {files}")
            response = self.session.post(url, files=files)

        if not response.ok:
            raise APIError(response)

    def __del__(self):
        self.log.debug("closing session")
        self.session.close()


class _DummyTag:
    """
    Minimal mock implementation of bs4.element.Tag (only has text attribute)

    >>> eg = _DummyTag('some text')
    >>> eg.text
    'some text'
    """
    def __init__(self, text):
        self.text = text


class JSSErrorParser(html.parser.HTMLParser):
    """
    Minimal mock implementation of bs4.BeautifulSoup()

    >>> [t.text for t in JSSErrorParser(html).find_all('p')]
    ['Unauthorized', 'The request requires user authentication',
     'You can get technical details here. {...}']
    """
    def __init__(self, html):
        super().__init__()
        self._data = {}
        if html:
            self.feed(html)

    def find_all(self, tag):
        """
        Minimal mock implemetation of BeautifulSoup(html).find_all(tag)

        :param tag <str>:   html tag
        :returns <list>:    list of _DummyTags
        """
        return self._data.get(tag, [])

    def handle_data(self, data):
        """
        override HTMLParser().handle_data()
            (automatically called during HTMLParser.feed())
        creates _DummyTag with text attribute from data
        """
        self._dummytag = _DummyTag(data)

    def handle_endtag(self, tag):
        """
        override HTMLParser().handle_endtag()
            (automatically called during HTMLParser.feed())
        add _DummyTag object to dictionary based on tag
        """
        # only create new list if one doesn't already exist
        self._data.setdefault(tag, [])
        self._data[tag].append(self._dummytag)


def parse_html_error(html):
    """
    Get meaningful error information from JSS Error response HTML

    :param html <str>:  JSS HTML error text
    :returns <list>:    list of meaningful error strings
    """
    if not html:
        return []
    try:
        soup = BeautifulSoup(html, features="html.parser")
    except NameError:
        # was unable to import BeautifulSoup
        soup = JSSErrorParser(html)
    # e.g.: ['Unauthorized', 'The request requires user authentication',
    #        'You can get technical details here. (...)']
    # NOTE: get first two <p> tags from HTML error response
    #       3rd <p> is always 'You can get technical details here...'
    return [t.text for t in soup.find_all('p')][0:2]


def file_mime_type(path):
    """
    Uses `/usr/bin/file` to determine mime-type (requires Developer Tools)

    :param path <str>:  Path to file
    :returns str:       content type of file
    """
    cmd = ['/usr/bin/file', '-b', '--mime-type', path]
    return subprocess.check_output(cmd).rstrip()
