#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Patch based classes
"""

import logging

# from .jss import JSS
from . import convert

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"


class DefinitionError(Exception):
    pass


class Policy(object):
    pass
    

class Grouping(object):
    pass


class Scope(Grouping):
    
    @property
    def all(self):
        pass
    
    def buildings(self):
        pass
    
    def users(self):
        pass
    
    def computers(self):
        pass
    
    def groups(self):
        pass
    
    def exclusions(self):
        pass
        
    def limitations(self):
        pass
    
    def departments(self):
        pass


class Limitation(Grouping):
    
    def ibeacons(self):
        pass
    
    def network(self):
        pass


class Exclusion(Grouping):
    
    def buildings(self):
        pass
    
    def groups(self):
        pass
    
    def departments(self):
        pass
    
    def ibeacons(self):
        pass
    
    def network(self):
        pass
    
    def users(self):
        pass



class PatchPolicy(object):
    
    def __init__(self, jss):
        self.jss = jss
        self.name = None
        self.scope = None
        self.version = None
        self.jssid = None


class SoftwareTitle():
    
    def __init__(self, jss, jssid):
        endpoint = f"patchsoftwaretitles/id/{jssid}"
        self.jss = jss
        self.jssid = jssid
        self.info = jss.get(endpoint)

    def patch_policies(self):
        endpoint = f"patchpolicies/softwaretitleconfig/id/{self.jssid}"
        result = self.jss.get(endpoint)['patch_policies']
        return result['patch_policy']


class SoftwareTitles():
    
    def __init__(self, jss):
        endpoint = 'patchsoftwaretitles'
        self.jss = jss
        result = self.jss.get(endpoint)['patch_software_titles']
        self.titles = result['patch_software_title']
#         for t in result['patch_software_title']:
#             result = jss.get(f"patchsoftwaretitles/id/{t['id']}")
#             self.titles.append(result['patch_software_title'])
        # self.titles = result['patch_software_title']

    def find(self, name):
        for title in self.titles:
            if title['name'] == name:
                jssid = title['id']
                info = self.jss.get(f"patchsoftwaretitles/id/{jssid}")
                return info['patch_software_title']
  
class Version(object):

    def __init__(self, pkg=None):
        self.package = pkg


class Package():
    
    def __init__(self, jssid, name):
        self.jssid = jssid
        self.name = name
    
    def _parse(self, name):
        _name = name
        while 'pkg' in _name:
            _name = os.path.splitext(_name)[0]
        *name, version, date, initials = _name.split(_name)
        # name, version, date, who, ext


def parse_pkg_name(pkg):
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
    

def new_software_title(jss, name, source):
    pass
    

class PatchManagement(object):
    """
    Class representing PatchManagement 
    """
    def __init__(self, jss, policy):
        self.jss = jss
        # tie-in to base policy
        self.policy = policy

    def titles(self):
        """
        List of existing software titles
        """
        endpoint = 'patchsoftwaretitles'
        
        
    def patch_policies(self):
        """
        List of patch policies
        """
        pass

    def definition(self):
        """
        versions and their packages
        """
        pass

    def alpha(self):
        """
        latest version
        """
        pass
    
    def beta(self):
        """
        testing version
        """
        pass
    
    def stable(self):
        """
        stable version (should mirror base policy)
        """
        pass

    def versions(self):
        """
        list of versions for Patch
        """
        pass
        
    def category(self):
        """
        category of app (should mirror base policy)
        """
        pass

    def name(self):
        pass


class TitleDefinition(object):
    """
    Class for representing Title Definition (may be overkill)
    """
    def __init__(self, data):
        self.name = data['app_name']
        self.version = data['current_version']
        self.publisher = data['publisher']
        self.modified = data['last_modified']
        self.ID = data['name_id']


class AvailableTitles(object):

    def __init__(self, jss, sourceid):
        self.log = logging.getLogger(f"{__name__}.AvailableTitles")
        self.jss = jss
        self.sourceid = sourceid
        self._titles = None
    
    @property
    def titles(self):
        """
        :returns: list of available titles from sourceID
        """
        if not self._titles:
            self.log.info("updating patch definitions")
            # current headers
            _headers = self.jss.session.headers
            # json doesn't seem to work with 'patchavailabletitles'
            self.jss.session.headers.update({'Accept': 'application/xml'})
            endpoint = f"patchavailabletitles/sourceid/{self.sourceid}"
            result = self.jss.get(endpoint)
            # restore previous headers
            self.jss.session.headers = _headers
            titles = convert.xml_to_dict(result)['patch_available_titles']
            self._titles = titles['available_titles']['available_title']
        return self._titles

    def find(self, name):
        for title in self.titles:
            if name == title['app_name']:
                # return TitleDefinition(title)
                return title
        raise DefinitionError(f"missing definition: {name}")


if __name__ == '__main__':
    pass