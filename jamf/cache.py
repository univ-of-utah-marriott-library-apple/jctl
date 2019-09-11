#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
caching for JSS
"""

import logging
import pickle
import os
import shutil

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"

class Error(Exception):
    pass

class CacheError(Error):
    pass


class Manager(object):
    
    def __init__(self, directory):
        #shutil.rmtree(directory)
        self.log = logging.getLogger(f"{__name__}.Manager")
        self.directory = directory
        if not os.path.exists(directory):
            self.log.debug(f"creating cache directory: {directory}")
            os.mkdir(directory)
        self._caches = {}
        # for name in os.listdir(directory):
        #     path = os.path.join(directory, name)
        #     self.log.debug(f"loading existing cache: {path}")
        #     self._caches[name] = Cache(path)

    def retrieve(self, endpoint):
        key = endpoint.replace('/', '-')
        # get existing cache, or create one if missing
        self.log.debug(f"retrieving: '{endpoint}'")
        try:
            _cache = self._caches[key]
        except KeyError as e:
            self.log.debug(f"cache not loaded: '{endpoint}'")
            path = os.path.join(self.directory, key)        
            _cache = Cache(path)
            self._caches[key] = _cache
        return _cache.data

    def update(self, endpoint, data):
        key = endpoint.replace('/', '-')
        # get existing cache, or create one if missing
        self.log.debug(f"updating: {endpoint!r}")
        _cache = self._caches.get(key)
        if not _cache:
            path = os.path.join(self.directory, key)
            _cache = self._caches.setdefault(key, Cache(path))
        _cache.update(data)
    
    def clear(self):
        self.log.debug("clearing caches")
        for _cache in self._caches.values():
            _cache.clear()
        self._cache = {}
        os.rmdir(self.directory)
        os.mkdir(self.directory)


class Cache(object):
    """
    """
    def __init__(self, path):
        self.log = logging.getLogger(f"{__name__}.Cache")
        self.log.debug("initializing")
        self.path = path
        self.data = {}
        self._modified = False
        if os.path.exists(path):
            self.log.debug(f"loading existing cache: {path}")
            self.read()
            # self.data = pickle.load(path, encoding="utf-8")
            # self.data = self.read()
        else:
            self.log.debug(f"no existing cache")
    
    def write(self, data=None):
        self.log.debug(f"pickling: {self.path}")
        if not data:
            data = self.data
        with open(self.path, 'wb') as f:
            pickle.dump(data, f)
        self._modified = False

    def read(self):
        if not os.path.exists(self.path):
            raise CacheError(f"cache missing: {self.path}")
        self.log.debug(f"loading pickle: {self.path}")
        with open(self.path, 'rb') as f:
            self.data = pickle.load(f, encoding='utf-8')
        # self.log.debug(f"data loaded: {self.data!r}")
        return self.data

    def update(self, data):
        """
        update cache on disk
        """
        self._modified = True
        self.log.debug(f"path: {self.path}")
        self.data = data
        self.write(data)
        
    def clear(self):
        """
        reset cache and delete existing file
        """
        self.log.debug(f"removing cache: {self.path}")
        self.data = {}
        try:
            os.remove(self.path)
        except OSError as e:
            if e.errno == 2:
                pass
        
    def __del__(self):
        if self.data and self._modified:
            self.write()
        elif not self.data and os.path.exists(self.path):
            self.clear()


if __name__ == '__main__':
    pass