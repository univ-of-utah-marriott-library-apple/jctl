# -*- coding: utf-8 -*-

# import os
# import logging
import plistlib
import unittest
import pprint

from ..jss import JSS
from .. import patch
# from .. import convert

class BaseTestCase(unittest.TestCase):
    pass


class TestAvailableTitles(BaseTestCase):
    
    @classmethod
    def setUpClass(cls):
        config = plistlib.readPlist('private/jss')
        auth = config['login'].split(':')
        address = config['address']
        #print(f"auth: {address}")
        cls.jss = JSS(address, auth=auth)
        # print(cls.jss)
    
    def setUp(self):
        self.jss = self.__class__.jss
        #print(self.jss)
        self.titles = patch.AvailableTitles(self.jss, 2)
    
    def test_titles(self):
        
        # result = convert.xml_to_dict(self.xml)
        pprint.pprint(self.titles.titles)


if __name__ == '__main__':
    # fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    # logging.basicConfig(level=logging.DEBUG, format=fmt)
    unittest.main(verbosity=1)