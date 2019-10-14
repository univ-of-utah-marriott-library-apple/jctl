# -*- coding: utf-8 -*-

# import os
# import logging
import pprint
import plistlib
import unittest
import logging

from .. import api
from .. import policies

API = None

def setUpModule():
    with open('private/jss.plist', 'rb') as f:
        config = plistlib.load(f)
    user, passwd = config['login'].split(':')
    global API
    API = api.API(config['address'], (user, passwd))


class BaseTestCase(unittest.TestCase):
    pass


class TestBlankPolicy(BaseTestCase):
        
    def setUp(self):
        self.policy = policies.Policy(API)
    
    def test_is_not_none(self):
        self.assertIsNotNone(self.policy)

    def test_xml(self):
        expected = '<policy></policy>'
        self.assertEqual(expected, self.policy.xml())


class TestCategories(BaseTestCase):
    
    def setUp(self):
        # mock category data
        self.data = [{'id': '1', 'name': 'name-1'},
                     {'id': '2', 'name': 'name-2'},
                     {'id': '3', 'name': 'Name-1'},
                     {'id': '4', 'name': 'different'}]

        # mock api object (returns data above)
        class MockAPI:
            def __init__(self, c):
                self.c = c
            def get(self, *args, **kwargs):
                return {'categories': {'category': self.c}}
        
        self.api = MockAPI(self.data)
        # function being tested
        self.func = policies.categories
        
    def test_categories(self):
        """
        test all categories are returned
        """
        result = self.func(self.api)
        expected = self.data
        self.assertEqual(expected, result)

    def test_category_name(self):
        """
        test categories matching name are returned
        """
        result = self.func(self.api, name='name')
        expected = [{'id': '1', 'name': 'name-1'}, 
                    {'id': '2', 'name': 'name-2'}]
        self.assertEqual(expected, result)

    def test_category_name_exclude_tuple(self):
        """
        test exclude as tuple
        """
        result = self.func(self.api, name='name', exclude=('name-1',))
        expected = [{'id': '2', 'name': 'name-2'}]
        self.assertEqual(expected, result)

    def test_category_name_exclude_list(self):
        """
        test exclude as list
        """
        result = self.func(self.api, name='name', exclude=['name-1'])
        expected = [{'id': '2', 'name': 'name-2'}]
        self.assertEqual(expected, result)

    def test_category_name_exclude_set(self):
        """
        test exclude as set
        """
        result = self.func(self.api, name='name', exclude=set(['name-1']))
        expected = [{'id': '2', 'name': 'name-2'}]
        self.assertEqual(expected, result)

    def test_category_name_exclude_same(self):
        """
        test same name and exclude returns empty list
        """
        result = self.func(self.api, name='name-2', exclude=('name-2',))
        expected = []
        self.assertEqual(expected, result)


def main():
    pass


if __name__ == '__main__':
    fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    unittest.main(verbosity=1)
    # main()