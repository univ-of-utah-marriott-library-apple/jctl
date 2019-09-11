#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JSS api
"""

import logging

from . import jss

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"


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


class Patch(object):
    
    def __init__(self, data):
        


if __name__ == '__main__':
    pass