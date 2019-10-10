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
    

if __name__ == '__main__':
    pass
