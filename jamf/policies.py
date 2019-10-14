# -*- coding: utf-8 -*-

"""
JAMF Policy functions
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"

import logging

from . import convert

LOGGER = logging.getLogger(__name__)

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
    

class Policy(object):

    def __init__(self, api, jssid=None):
        self.log = logging.getLogger(f"{__name__}.Policy")
        self.api = api
        self._jssid = jssid
        self._name = None
        self.enabled = None
        self._scope = None
        self._modified = False

        if jssid:
            self.data = api.get(f"policies/id/{jssid}")['policy']
        else:
            self._general = {}
            self.data = {}

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
    
    def packages(self):
        pass
    
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


# def categories(jss, name=None):
#     """
#     :returns: list of all categories
#     """
#     _categories = jss.get('categories')['categories']['category']
#     if name is not None:
#         return [x for x in _categories if name in x['name']]
#     else:
#         return _categories


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


def app_policy_template(appname, category_name, scope):
    category = CATEGORY[category_name]
    return {'policy': {'general': {'name': name,
                                   'frequency': 'Ongoing',
                                   'category': category,
                                   'trigger_other': 'lab_software'},
                        'scope': scope,
                        'scripts': {'script': {'id': '66',
                                               'parameter4': f"Installing {name}",
                                               'priority': 'Before'}},
                        'self_service': {'use_for_self_service': 'true'}
                                   }}


def new_app_policy(api, name):
    """
    workflow of creating a new app policy
    """
    # questions:
    # what does a base-minimum new policy look like?
    raise NotImplementedError("not yet finished")
    all_policies = api.get('policies')
    matching = []
    for p in all_policies['policies']:
        if name in p['name']:
            matching.append(p)
    
    return matching
    # requirements:
    # - name
    # - category
    # - package
    # - icon
    # - scope
    # - 
    pass


def test_policy_modification(api, jssid, icon):
    """
    Verify setting some values adjust others
    """
    existing = api.get(f"policies/id/{jssid}")['policy']

    # upload icon if it's missing
    if not existing['self_service']['self_service_icon']:
        api.upload(f"policies/id/{jssid}", icon)
    
    category = CATEGORY['Apps - Office']
    policy = {'general': {'category': category},
              'self_service': {
                'self_service_categories': {'category': category}}
              }
    result = api.put('policies/id/453', {'policy': policy})
    pprint.pprint(result)


def new_policy_workflow(api):
    name = None
    icon = None
    package = None
    category = None
    template = None
    timestamp = None
    
    # create_app_policy(api, name)
    # template = app_policy_template(name)
    # result = api.post('policies/id/0', template)
    # pprint.pprint(result)
    # result = api.get('policies/id/453')
    # return result
    pass


def verify_policy(policy):
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
        
