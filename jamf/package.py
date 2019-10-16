# -*- coding: utf-8 -*-

"""
JAMF Packages
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"

import re
import logging
import plistlib
import hashlib
import datetime as dt

# GLOBALS
LOGGER = logging.getLogger(__name__)


class Error(Exception):
    pass


class JDS(object):
    """
    Jamf Distribution Server
    """

    def __init__(self, address, auth):
        """
        """
        self.log = logging.getLogger(f"{__name__}.JDS")
        self.address = address
        self.auth = auth
        self.path = None
        self._mounted = None

    def mount(self):
        """
        Mount the Jamf Distribution Server
        """
        raise NotImplementedError()
        if self._mounted:
            self.log.error("JDS already mounted")
            return

    def packages(self):
        """
        :returns: list of packages on JDS
        """
        raise NotImplementedError()
        
    def upload(self, pkg):
        """
        Add package to JDS 
        """
        raise NotImplementedError()

    def find(self, pkg):
        """
        Locate package on JDS
        """
        raise NotImplementedError()
        

class Manager(object):
    """
    Package Manager
    """

    def __init__(self, config):
        self.log = logging.getLogger(f"{__name__}.Manager")
        self.config = config
        jds = self.config['JDS']
        self.jds = JDS(jds['address'], jds['authentication'])
    
    def find(self, name):
        """
        :param name:        name of package
        :returns Package:  
        """
        raise NotImplementedError()
    
    def upload(self, pkg):
        """
        Upload package to JDS and create new database entry
        """
        raise NotImplementedError()
    
    
class Package(object):
    """
    Experimental: NOT IN USE
    Base Package class 
    """
    def __init__(self, appname, name, version):
        self.appname = appname
        self.name = name
        self.version = version


class Record(object):
    """
    Class for local package records
    """
    def __init__(self, path):
        self.path = path
        self.app = None
        self.version = None
        self.uploaded = None
        self.indexed = None
        self.install_path = None
        
        if os.path.exists(path):
            self.load(path)

    def load(self):
        """
        load from disk
        """
        raise NotImplementedError()

    def save(self):
        """
        save to disk
        """
        raise NotImplementedError()
        

class LocalPackage(object):

    def __init__(self, record):
        pass


class JSSPackages(object):
    
    def __init__(self, api):
        self.log = logging.getLogger(f"{__name__}.ServerPackages")
        self.log.info("getting packages from server: {api.address!r}")
        self.packages = api.get('packages')['packages']['package']
    
    @property
    def names(self):
        """
        :returns: list of names of all packages
        """
        return [p['name'] for p in self.packages]
    
    def find(self, name):
        """
        :param name:    name of package
        :returns dict:  package information
        """
        for p in self.packages:
            if p['name'] == name:
                return p
        err = f"missing package: {name!r}"
        self.log.error(err)
        raise Error(err)


def verify(api, pkg):
    """
    Verify package on JSS

    :param api:  jamf.API object
    :param pkg:  Package object
    """
    raise NotImplementedError()


def parse_name_orig(name):
    """
    split package naming scheme into parts

    WARNING: not perfect

    :returns: "appname", "version", "date", "initials"
    
    >>> parse_pkg_name('name_of_app_1.0_2019.09.18_swf.pkg')
    'name_of_app', '1.0', '2019.09.18', 'swf'
    """

    # remove the extension until we get to the proper basename
    while 'pkg' in pkg: 
        pkg = os.path.splitext(name)[0]
    *name, version, date, initials = pkg.split('_')
    return "_".join(name), version, date, initials
    

def parse_name(name, regex):
    """
    split package naming scheme into parts

    WARNING: not perfect

    :returns: "appname", "version", "date", "initials"
    
    >>> parse_pkg_name('name_of_app_1.0_2019.09.18_swf.pkg')
    'name_of_app', '1.0', '2019.09.18', 'swf'
    """
    raise NotImplementedError()


def packages(api):
    """
    :returns: list of dictionaries for all packages on JSS
    """
    # Each entry is dict containing the following keys:
    # ['id',     # <int>  JSS id
    #  'name']   # <str> name of package
    return api.get('packages')['packages']['package']


def installer_packages():
    """
    quick and dirty dump of packages on InstallerPackages
    """
    vol = '/Volumes/InstallerPackages/munkipkg_projects'
    import glob
    g = os.path.join(vol, '*/payload/*.app')
    info = {}
    for path in glob.glob(g):
        name = os.path.splitext(os.path.basename(path))[0]
        directory = path.split('/payload')[0]
        folder = os.path.basename(directory)
        pkgs = []
        for pkg in glob.glob(os.path.join(directory, 'build/*.pkg')):
            pkgs.append(os.path.basename(pkg))

        plist = os.path.join(directory, 'build-info.plist')
        with open(plist, 'rb') as f:
            b_info = plistlib.load(f)

        info[name] = {'pkgs': pkgs, 'folder': folder, 
                      'build': b_info, 'name': name}
    
    pprint.pprint(info)


def md5(path):
    """
    :returns: md5 checksum of path
    """
    md5 = hashlib.md5()
    with open(path, 'rb') as f: 
        for chunk in iter(lambda: f.read(8192), b''): 
            md5.update(chunk)
    return md5.digest()


if __name__ == '__main__':
    pass
