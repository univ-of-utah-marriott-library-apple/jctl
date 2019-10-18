# -*- coding: utf-8 -*-

"""
JAMF Policy functions
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"

import os
import logging

from . import convert
from .api import APIError

# GLOBALS
LOGGER = logging.getLogger(__name__)
CATEGORY = {
    'Apps - Admin Utilities': {'id': 40, 'name': 'Apps - Admin Utilities'},
    'Apps - Audio': {'id': 47, 'name': 'Apps - Audio'},
    'Apps - Chat': {'id': 7, 'name': 'Apps - Chat'},
    'Apps - Educational': {'id': 48, 'name': 'Apps - Educational'},
    'Apps - Games': {'id': 49, 'name': 'Apps - Games'},
    'Apps - Graphical': {'id': 15, 'name': 'Apps - Graphical'},
    'Apps - Imaging': {'id': 3, 'name': 'Apps - Imaging'},
    'Apps - Internet': {'id': 8, 'name': 'Apps - Internet'},
    'Apps - Office': {'id': 14, 'name': 'Apps - Office'},
    'Apps - Programming': {'id': 39, 'name': 'Apps - Programming'},
    'Apps - Science': {'id': 50, 'name': 'Apps - Science'},
    'Apps - Utilities': {'id': 2, 'name': 'Apps - Utilities'},
    'Apps - Video': {'id': 44, 'name': 'Apps - Video'},
    'Apps - Web Browsers': {'id': 1, 'name': 'Apps - Web Browsers'},
}


class Error(Exception):
    pass


class Trigger(object):

    def __init__(self):
        self.ongoing = None
        self.offline = None
        self.events = None
        self.custom = None


class Scope(object):
    
    def __init__(self):
        self.target = None
        self.exclusions = None
        self.limitations = None
    

class Script(object):

    def __init__(self, name, priority, parameters):
        self.name = name
        self.priority = priority # Before || After
        self.parameters = parameters


class Scripts(object):
    
    def add(self, x):
        pass
    
    def remove(self, x):
        pass


class Packages(object):
    pass


class SelfService(object):

    def __init__(self):
        self.icon = None
        self.description = None
        self.name = None
        self.notification = None
        self.enabled = None
        self.featured = None
        self.categories = None
        self.buttons = None


class Policy(object):

    def __init__(self, api, jssid=None, name=None):
        self.log = logging.getLogger(f"{__name__}.Policy")
        self.api = api

		self.data = {}
		self._general = {}
        self._name = None
        self.enabled = None
        self._scope = None
        self._modified = False

		if name:
			self._name = name
            self.data = api.get(f"policies/name/{name}")['policy']
        elif jssid:
			self._jssid = jssid
            self.data = api.get(f"policies/id/{jssid}")['policy']
		else:
			raise Error("must specify name or jssid")


    @property
    def jssid(self):
        return self._jssid

    @property
    def name(self):
        return self._data['general']
    
    @name.setter
    def name(self):
        pass
       
    @property
    def category(self):
        return self._data['general']['category']

    @category.setter
    def category(self, c):
        self._modified = True
        self._data['general']['category'] = c

    @property
    def modified(self):
        pass
    
    def scripts(self):
        pass
    
    def scope(self):
        pass
    
    def replace_package(self, old, new):
    	pass
    
    def add_package(self, name):
    	pass
    
    def remove_package(self, name):
    	pass
    	
    def packages(self):
        """
		:returns: existing policy packages (if any)
        """
        
        
    
    def selfservice(self):
        pass
    
    def enable(self):
        pass

    def disable(self):
        pass

    def create(self):
        if self.jssid:
            raise Error(f"policy already exists: ID: {self.jssid}")
    
    def update(self, data):
        pass
    
    def submit(self):
        pass
    
    def xml(self):
        return convert.dict_to_xml({'policy': self.data})


# jamf.policy.replace_package(api, policy, old, new)?

# jamf.Policy(api, name="Office").replace_package("Office 2016", "Office 2019")?

# p = jamf.Policy(api, name="Office")
# p.replace_package("Office 2016", "Office 2019")

def replace_package(self, old, new):
	pass

def add_package(self, name):
	pass

def remove_package(self, name):
	pass
	
def packages(self):
	"""
	:returns: existing policy packages (if any)
	"""


def categories(api, name='', exclude=()):
    """
    Get JSS Categories

    :param api:  jamf.api.API object
    :param name  <str>:      name in category['name']    
    :param exclude  <iter>:  category['name'] not in exclude
    
    :returns:  list of dicts: [{'id': jssid, 'name': name}, ...]
    """
    # list of category dicts: [{'id': id, 'name': name}, ...]
    _categories = api.get('categories')['categories']['category']
    # exclude specified categories by full name
    included = [c for c in _categories if c['name'] not in exclude]
    #NOTE: empty string ('') always in all other strings
    return [c for c in included if name in c['name']]


def policies_in_categories(api, categories):
    """
    Get list of policies in specified categories

    :param api:         jamf.API object
    :param categories:  list of category names
    :returns:           list of all policies from specified categories
    """
    LOGGER.debug(f"categories: {categories}")
    policies = []
    for c in categories:
        result = api.get(f"policies/category/{c}")['policies']
        policies += result.get('policy', [])
    
    return policies


def app_policies(api, exclude=()):
    """
    Get all policies from categories starting with 'Apps -'
    CAVEAT: requires naming scheme 
    :returns: list of installation policies
    """
    
    _app_categories = [x['name'] for x in categories(api, 'Apps -')]
    return policies_in_categories(api, _app_categories)


def default_app_scripts(name):
    """
    :returns: default scripts for app policies
    """
    logger = logging.getLogger(__name__)
    logger.warning(f"using hard-coded scripts")
    return {'script': {'id': '66', 'priority': 'Before',
                       'parameter4': f"Installing {name}"}}

    
def self_service(name, desc=None, icon=None):
    """
    :returns: template for self service
    """
    _template = {'self_service_display_name': name,
                 'use_for_self_service': 'true'}
    if desc:
        _template['self_service_description'] = desc
    if icon:
        _template['self_service_icon'] = icon

    return _template


def app_policy_template(name, category, trigger=None):
    """
    :returns: slightly populated application policy template
    """
    # TO-DO: create Policy class with configuration file for defaults
    # default trigger
    logger = logging.getLogger(__name__)
    logger.debug("building app policy template")
    custom_trigger = trigger or 'lab_software'

    general = {'name': name,
               'enabled': 'true',
               'frequency': 'Ongoing',
               'category': CATEGORY[category],
               'trigger_other': custom_trigger}
    
    # get scoping
    logger.warning("using hard-coded scoping")
    groups = [{'id': '219', 'name': '+ 10.14 OS'},
              {'id': '222', 'name': '+ 10.15 OS'}]
    scoping = {'computer_groups': {'computer_group': groups}}

    _template = {'general': general,
                 'scope': scoping,
                 'scripts': default_app_scripts(name),
                 'self_service': {'use_for_self_service': 'true'}}

    return {'policy': _template}

   
def new_app_policy(api, name, category, pkgs, icon, desc=None, scripts=None):
    """
    Create new app policy

    TO-DO: check for existing icon
    """
    logger = logging.getLogger(__name__)
    # check for existing policy
    try:
        logger.debug(f"checking for existing policy: {name}")
        policy = api.get(f"policies/name/{name}")
        logger.error(f"found existing policy: {name}")
        return policy
    except APIError as e:
        pass
    
    template = app_policy_template(name, category)
    template
    logger.info(f"creating new app policy: {name}")
    jssid = api.post('policies/id/0', template)['policy']['id']
    logger.debug(f"successfully created: {name} (id: {jssid})")
    
    endpoint = f"policies/id/{jssid}"
    # upload icon (if necessary?)
    logger.info(f"uploading icon: {icon}")
    api.upload(endpoint, icon)
    logger.debug(f"icon successfully uploaded")
    
    update_app_policy(api, jssid, pkgs, desc, scripts)


def update_app_policy(api, jssid, pkgs, desc=None, scripts=None):
    """
    Designed to update newly created app policies

    NOTE: all modifications should be fully built (does not merge data)

    TO-DO: test description update
    """
    # logger = logging.getLogger(__name__)
    # NOTE: this is kludgy, but I don't want to modify pkgs from outside
    try:
        _pkgs = {k:v for k,v in pkgs.items()}
        _pkgs['action'] = 'Install'
    except AttributeError:
        if instance(pkgs, list):
            _pkgs = []
            for p in pkgs:
                n = {'action': 'Install'}
                n.update(p)
                _pkgs.append(n)

    mod = {'package_configuration': {'packages': {'package': _pkgs}}}
        
    # self service
    if desc:
        mod['self_service'] = {'self_service_description': desc}

    # add scripts
    if scripts:
        mod['scripts'] = scripts

    # upload changes
    changes = {'policy': mod}
    # return changes
    return api.put(f"policies/id/{jssid}", changes)



def verify(policy):
    """
    verify policy
    """
    logger = logging.getLogger(__name__)
    logger.warning("policy verification incomplete")
    # raise NotImplementedError("not finished")


def verification(jss, name, category, icon, pkgs, schema):
    """
    verification of entire stack
    """

    # App Policy
    #  - exists
    #  - category
    #  - scope
    #  - package
    #  - self service
    #   - icon
    #   - notifications
        # create app policy if missing
    
    # Package Verification
    #  - exists

    # External Patch Definition
    
    # Patch Software Title
    #   package
    #   version
    #   category
    
    # Patch Policies

    # Additional
    pass


def add_notify_script(api, jssid, modify=True):
    endpoint = f"policies/id/{jssid}"
    policy = api.get(endpoint)['policy']
    # return policy
    name = policy['general']['name']
    # empty: {'scripts': {'size': '0'}}
    # single: {'scripts': {'script': {'id': '66',
    #                                 'name': 'Notify.sh',
    #                                 'parameter10': None,
    #                                 'parameter11': None,
    #                                 'parameter4': 'Installing Amadeus Pro',
    #                                 'parameter5': None,
    #                                 'parameter6': None,
    #                                 'parameter7': None,
    #                                 'parameter8': None,
    #                                 'parameter9': None,
    #                                 'priority': 'Before'},
    #                       'size': '1'}}
    # multiple:  'scripts': {'script': [{'id': '66',
    #                                    'name': 'Notify.sh',
    #                                    'parameter10': None,
    #                                    'parameter11': None,
    #                                    'parameter4': 'Installing Dropbox',
    #                                    'parameter5': None,
    #                                    'parameter6': None,
    #                                    'parameter7': None,
    #                                    'parameter8': None,
    #                                    'parameter9': None,
    #                                    'priority': 'Before'},
    #                                   {'id': '72',
    #                                    'name': 'remove path',
    #                                    'parameter10': None,
    #                                    'parameter11': None,
    #                                    'parameter4': '/Library/DropboxHelperTools',
    #                                    'parameter5': None,
    #                                    'parameter6': None,
    #                                    'parameter7': None,
    #                                    'parameter8': None,
    #                                    'parameter9': None,
    #                                    'priority': 'Before'}],
    #                       'size': '2'}}
    notify_id = '66'
    notify = {'id': notify_id, 'priority': 'Before', 
              'parameter4': f"Installing {name}"}
    
    size = int(policy['scripts']['size'])
    if size == 0:
        # no existing scripts (can replace)
        scripts = notify
    elif size == 1:
        # single existing script
        existing = policy['scripts']['script']
        if existing['id'] != notify_id:
            # add notify to existing script
            scripts = [existing, notify]
        else:
            scripts = notify
    else:
        # multiple scripts
        existing = policy['scripts']['script']
        other = [x for x in existing if x['id'] != notify_id]
        scripts = other + [notify]
            
    data = {'scripts': {'script': scripts}}

    if modify:
        return api.put(endpoint, {'policy': data})
    else:
        return data


def add_script(scripts, script):
    size = int(scripts['size'])
    
    if size == 0:
        # no existing scripts (can replace)
        new = script
    elif size == 1:
        # single existing script (dictionary)
        existing = scripts['script']
        if scripts['script']['id'] != script['id']:
            # add script to existing script (modifies type to list)
            new = [scripts['script'], script]
        else:
            new = script
    else:
        # multiple scripts (list of dictionaries)
        other = [x for x in scripts['script'] if x['id'] != script['id']]
        new = other + [script]
            
    return {'script': new}


def add_custom_trigger(general, trigger, replace=False):
    if not general['trigger_other']:
        return {'trigger_other': trigger}


def modify(api, jssid, data):
    """
    recursive modification of policy?
    """
    pass
    

def quick_modify(api):
    """
    recursive modification of policy?
    """
    # result = []
    logger = logging.getLogger(__name__)
    
    for p in app_policies(api):
        endpoint = f"policies/id/{p['id']}"
        policy = api.get(endpoint)['policy']
        name = policy['general']['name']

        if policy['general']['enabled'] == 'false':
            logger.info(f"skipping disabled policy: {name}")
            continue

        mod = {}
        
        # modify scripts
        s = {'id': '66', 'priority': 'Before', 
             'parameter4': f"Installing {name}"}
        mod['scripts'] = add_script(policy['scripts'], s)

        # modify custom triggers
        trigger = policy['general']['trigger_other']
        if not trigger:
            mod['general'] = {'trigger_other': 'lab_software'}
        elif 'software' not in trigger:
            m = f"Policy: {name} (ID: {p['id']}): has trigger: {trigger}"
            logger.warning(m)
        
        # submit changes
        try:
            logger.info("updating: {name}")
            api.put(endpoint, {'policy': mod})
        except jamf.api.Error as e:
            logger.error(f"{name}: failed: {e}")
        # result.append({'policy': mod})
    # return result
    pass
        
