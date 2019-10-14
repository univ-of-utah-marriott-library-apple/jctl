# -*- coding: utf-8 -*-

"""
JAMF Packages
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"

import logging


class Error(Exception):
    pass

    
class Package(JSSObject):
    """
    Experimental class (not in use)
    """
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.jssid = None
        self.uploaded = None
        self.indexed = None
        self.category = None
    
    def upload(self):
        pass
    
    def index(self):
        pass
    

class Version(object):

    def __init__(self, pkg=None):
        self.package = pkg



class PackageOrig(object):
    
    def __init__(self, jssid, name):
        self.jssid = jssid
        self.name = name
    
    def _parse(self, name):
        _name = name
        while 'pkg' in _name:
            _name = os.path.splitext(_name)[0]
        *name, version, date, initials = _name.split(_name)
        # name, version, date, who, ext


def parse_pkg_name(name):
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




if __name__ == '__main__':
    pass
