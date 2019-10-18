#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility for installing packages and installation information
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"

import os
import sys
import logging
import plistlib
import subprocess
import datetime as dt


class Error(Exception):
    pass


class Record(object):
    
    def __init__(self, path, data=None):
        self.log = logging.getLogger(f"{__name__}.Record")
        self.path = path
        self.data = None
        if os.path.exists(path):
            self.load()
        self.data = data or {}
    
    def load(self):
        self.log.debug("loading: %r", self.path)
        with open(self.path, 'rb') as f:
            self.data = plistlib.load(f)
            return self.data
    
    def save(self):
        self.log.debug("saving: %r", self.path)
        with open(self.path, 'wb') as f:
            plistlib.dump(self.data, f)

    def update(self, key, data):
        self.log.debug("updating: %r", key)
        self.data.setdefault(key, {})
        self.data[key].update(data)

    def append(self, key, data):
        self.log.debug("appending: %r", key)
        self.data.setdefault(key, [])
        self.data[key].append(data)

    def merge(self, data):
        pass


class Package(object):
    
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        

def info(pkgpath):
    """
    :returns: information about package
    """
    raise NotImplementedError()


def find_app(name, location='/Applications'):
    """
    :returns: absolute path to application by name
    """
    logger = logging.getLogger(__name__)
    logger.debug("searching for %r", name)
    name = name.strip('.app')
    search = f"kMDItemKind == 'Application' && kMDItemDisplayName == '{name}'"
    cmd = ['/usr/bin/mdfind', '-onlyin', location, search]
    logger.debug("%r", cmd)
    try:
        out = subprocess.check_output(cmd).rstrip()
        return out.decode('utf-8')
    except subprocess.CalledProcessError:
        logger.error("unable to locate app: %r", name)
        raise
        

def app_info(path):
    """
    :returns: dictionary of various components used by patch management
    """
    logger = logging.getLogger(__name__)
    plist = os.path.join(path, 'Contents/Info.plist')
    logger.debug("reading: %r", plist)
    with open(plist, 'rb') as f:
        info = plistlib.load(f)
    
    keys = ('CFBundleVersion', 'CFBundleShortVersionString', 
            'CFBundleIdentifier', 'LSMinimumSystemVersion')
    return {k:v for k,v in info.items() if k in keys}


def record_path(name, location='records'):
    """
    :returns: path of record plist via name
    """
    return os.path.join(location, f"{name}.plist")


def pkg_name_info(name, callback=None):
    """
    Institutionally specific package naming function
    
    :param callback: function to execute for deriving package name information
    :returns: w/ keys 'author', 'version', 'created'
    """
    if not callback:
        def _callback(name):
            *_, v, d, a = os.path.splitext(name)[0].split('_')
            return {'version': v,
                    'created': dt.datetime.strptime(d, '%Y.%m.%d'),
                    'author': a}
        callback = _callback
    return callback(name)


def main(argv):
    logger = logging.getLogger(__name__)
    # result = app_info('/Applications/Programming/BBedit.app')
    try:
        # appname = os.path.basename(argv[0]).strip('.app')
        path = argv[0]
    except IndexError:
        raise SystemExit("must specify path")

    try:
        pkg = os.path.basename(argv[1])
    except IndexError:
        raise SystemExit("must specify pkg")

    if not os.path.exists(path):
        raise SystemExit(f"No such application: {path!r}")
    
    app = os.path.basename(path)
    name = app.strip('.app')
    r = Record(record_path(name, location='../../Desktop'))
    try:
        r.load()
    except FileNotFoundError:
        pass
        
    packages = r.data.setdefault('packages', {})
    
    info = pkg_info(pkg)
    # info = pkg_info(pkg)
    info.update({'info': app_info(path)})
    packages.update({pkg: info})
    r.save()
    # result = find_app('BBEdit')
    # print(repr(result))



if __name__ == '__main__':
    fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    main(sys.argv[1:])