# -*- coding: utf-8 -*-

"""
Unittests
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"

import shutil
import os
import unittest
import pprint

from .. import template
from .. import api

# location for temporary files created with tests
LOCATION = os.path.join(os.path.dirname(__file__))
TMPDIR = os.path.join(LOCATION, 'tmp', 'template')


def setUpModule():
    """
    One time setup for entire module. 
    If exception is raised, no tests in entire module are run.
    """
    # OPTIONAL
    if not os.path.exists(TMPDIR):
        os.makedirs(TMPDIR, mode=0o755)
    template.TEMPLATES = TMPDIR


def tearDownModule():
    """
    One time cleanup for entire module.
    """
    # OPTIONAL
    # shutil.rmtree(TMPDIR)
    shutil.rmtree(os.path.dirname(TMPDIR))


class TestLoadTemplate(unittest.TestCase):
    
    def setUp(self):
        self.name = 'loadingtest'
        self.data = {'test': 'test',
                     'name': self.name}
        self.path = os.path.join(TMPDIR, "{0}.plist".format(self.name))
        template.save_template(self.data, self.path)
    
    def test_load(self):
        result = template.load_template(self.name)
        expected = self.data
        self.assertEqual(expected, result)


class TestSaveTemplate(unittest.TestCase):
    
    def setUp(self):
        self.name = 'templatesavingtest'
        self.data = {'test': 'test', 
                     'name': self.name}
        self.path = os.path.join(TMPDIR, "{0}.plist".format(self.name))
    
    def test_save_without_path(self):
        """
        test data is saved from derived name
        """
        template.save_template(self.data)
        self.assertTrue(os.path.exists(self.path))

    def test_save_path(self):
        """
        test data is saved from derived name
        """
        template.save_template(self.data, self.path)
        self.assertTrue(os.path.exists(self.path))

    def test_save_without_path_missing_name(self):
        """
        test data is saved from derived name
        """
        del(self.data['name'])
        with self.assertRaises(KeyError):
            template.save_template(self.data)

        

class TestMergeTemplate(unittest.TestCase):
    pass


class TestTrimTemplate(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.api = api.API(config='private/jss.plist')
        cls.policy = cls.api.get('policies/id/345')['policy']
    
    def setUp(self):
        self.policy = self.__class__.policy
    
    def test_trim(self):
        result = template.trim_policy(self.policy)
        pprint.pprint(result)


   

if __name__ == '__main__':
    unittest.main(verbosity=1)
