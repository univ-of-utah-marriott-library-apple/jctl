# -*- coding: utf-8 -*-

"""
JAMF Packages
"""

import logging

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"

class Error(Exception):
    pass


class JSSObject(object):
    """
    NOT IN USE
    Experimental base JSS Object class
    a sort of pseudo dictionary
    """
    # defined XML schema
    # property: xml
    # str(obj.xml) returns xml string
    def __init__(self, d):
        """
        """
        # need list of GLOBAL jss keys
        self.jssid = None
        self._schema = None
        
    
    @property
    def xml(self):
        """
        Returns ElementTree of xml representation
        NOTE: only useful if str(self.xml) can be necessary xml string
        """
        raise NotImplementedError()
    

class Package(JSSObject):
    """
    Experimental class (not in use)
    """
    def __init__(self, jssid, name):
        self.name = name
        self.jssid = jssid

    @property
    def xml(self):
        values = f"<id>{self.jssid}</id>
                 f"<name>{self.name}</name>"
        return f"<package>{values}</package>"

