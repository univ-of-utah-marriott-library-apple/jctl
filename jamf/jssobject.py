# -*- coding: utf-8 -*-

"""
Base JSSObject (NOT IN USE)
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"

import logging

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
