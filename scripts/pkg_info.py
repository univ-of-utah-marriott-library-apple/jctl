#!/usr/local/bin/python3

import os
import sys
import logging
import plistlib
import pprint
import subprocess
import datetime as dt

## GLOBALS

LOGGER = logging.getLogger(__name__)

class Error(Exception):
    pass


class Record(object):
    
    def __init__(self, path, data=None):
        self.log = logging.getLogger(f"{__name__}.Record")
        self.path = path
        self.data = data or {}
    
    def load(self):
        self.log.debug(f"loading: {self.path!r}")
        with open(self.path, 'rb') as f:
            self.data = plistlib.load(f)
            return self.data
    
    def save(self):
        self.log.debug(f"saving: {self.path!r}")
        with open(self.path, 'wb') as f:
            plistlib.dump(self.data, f)

    def update(self, key, data):
        self.log.debug(f"updating: {key!r}")
        self.data.setdefault(key, {})
        self.data[key].update(data)

    def append(self, key, data):
        self.log.debug(f"appending: {key!r}")
        self.data.setdefault(key, [])
        self.data[key].append(data)


def find_app(name, location='/Applications'):
    """
    :returns: absolute path to application by name
    """
    LOGGER.debug("searching for %r", name)
    name = name.strip('.app')
    search = f"kMDItemKind == 'Application' && kMDItemDisplayName == '{name}'"
    cmd = ['/usr/bin/mdfind', '-onlyin', location, search]
    LOGGER.debug("%r", cmd)
    out = subprocess.check_output(cmd).rstrip()
    if not out:
        LOGGER.error("unable to locate app: %r", name)
    return out.decode('utf-8')


def app_info(path):
    """
    :returns: dictionary of various components used by patch management
    """
    plist = os.path.join(path, 'Contents/Info.plist')
    LOGGER.debug("reading: %r", plist)
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


def pkg_info(name):
    *_, ver, date, author = os.path.splitext(name)[0].split('_')
    created = dt.datetime.strptime(date, '%Y.%m.%d')
    return {'author': author, 
            'created': created, 'version': ver}

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
    #r.load()
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