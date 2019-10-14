#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Patch based classes
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"

import logging

# from .jss import JSS
from . import convert

LOGGER = logging.getLogger(__name__)

KINOBI = 2

PATCH_TEMPLATES = {
    'Adobe Flash Player': [{'name': 'Tech',
                            'method': 'prompt'},
                           {'name': 'Guinea Pig',
                            'method': 'prompt'},
                           {'name': 'Stable',
                            'method': 'prompt'}],
    'Apple Remote Desktop': [{'name': 'Tech - Test Boxes',
                              'method': 'prompt'},
                             {'name': 'Tech - Main Boxes',
                              'defer': 2,
                              'method': 'selfservice'}],
}

DEFAULT_PATCH = [{'name': 'Tech - Test Boxes',
                  'method': 'prompt'},
                 {'name': 'Tech - Main Boxes',
                  'defer': 2,
                  'method': 'selfservice'},
                 {'name': 'Guinea Pig - Lab',
                  'method': 'prompt'},
                 {'name': 'Guinea Pig - Staff',
                  'method': 'selfservice'},
                 {'name': 'Stable - Lab',
                  'method': 'prompt'},
                 {'name': 'Stable - Staff',
                  'method': 'selfservice'}]

STAGING = {'Tech': {'Main Boxes': {'id': 230, 
                                   'name': 'Staging - Tech Admin'},
                    'Test Boxes': {'id': 231, 
                                   'name': 'Staging - Tech Boxes'}},
           'Guinea Pig': {'Lab': {'id': 171, 
                                  'name': 'Staging - Guinea Pig - Lab'},
                          'Staff': {'id': 229,
                                    'name': 'Staging - Guinea Pig - Staff'}},
           'Stable': {'Lab': {'id': 234,
                              'name': 'Staging - Stable - Lab'},
                      'Staff': {'id': 233,
                                'name': 'Staging - Stable - Staff'}}}


class Error(Exception):
    pass


class DefinitionError(Error):
    pass


class MissingTitleError(Error):
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
    
    def __init__(self, api):
        endpoint = 'patchsoftwaretitles'
        self.jss = api
        result = self.api.get(endpoint)['patch_software_titles']
        self.titles = result['patch_software_title']
#         for t in result['patch_software_title']:
#             result = jss.get(f"patchsoftwaretitles/id/{t['id']}")
#             self.titles.append(result['patch_software_title'])
        # self.titles = result['patch_software_title']

    def find(self, name):
        for title in self.titles:
            if title['name'] == name:
                jssid = title['id']
                info = self.api.get(f"patchsoftwaretitles/id/{jssid}")
                return info['patch_software_title']


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
        self._titles = []
    
    @property
    def titles(self):
        """
        :returns: list of available titles from sourceID
        """
        if not self._titles:
            self.log.info("updating patch definitions")
            headers = {'Accept': 'application/xml'}
            endpoint = f"patchavailabletitles/sourceid/{self.sourceid}"
            result = self.jss.get(endpoint, headers=headers)
            self.log.debug(f"result: {result}")
            titles = result['patch_available_titles']
            self._titles = titles['available_titles']['available_title']
        return self._titles

    def find(self, name):
        for title in self.titles:
            if name == title['app_name']:
                return title
        raise MissingTitleError(f"missing definition: {name}")


class Notification(object):
    
    def __init__(self, policy, desc, deadline, grace_period=60):
        self.deadline = deadline
        self.grace_period = grace_period
        self.interaction = {'self_service_icon': {'id': icon_id},
                            'deadlines': {'deadline_enabled': True,
                                          'deadline_period': deferral}}
    def data(self):
        pass


def notification(name, version, desc, icon, defer, grace, nc=False):
    pass


def new_software_title(jss, name, source):
    pass
    



# FUNCTIONS

def softwaretitle_policies(api, jssid):
    """
    :returns: list of software title patch policies
    """
    endpoint = f"patchpolicies/softwaretitleconfig/id/{jssid}"
    return api.get(endpoint)['patch_policies']['patch_policy']


def policies(api, name=None):
    """
    :returns: list of all patch policies 
    """
    _policies = api.get('patchpolicies')['patch_policies']['patch_policy']
    if name is not None:
        return [x for x in _policies if name in x['name']]
    else:
        return _policies


def find_patch_definition(api, name, source=KINOBI):
    """
    :param api:     jamf API object
    :param name:    name of external patch definition
    :param source:  source ID of external patch server (default: patch.KINOBI) 

    :returns:       external patch definition by name
    """
    logger = logging.getLogger(__name__)
    LOGGER.info(f"looking for external definition: {name!r}")
    LOGGER.debug(f"patch source ID: {source}")
    endpoint = f"patchavailabletitles/sourceid/{source}"
    result = api.get(endpoint)['patch_available_titles']
    for title in result['available_titles']['available_title']:
        if name == title['app_name']:
            LOGGER.debug(f"found definition ID: {title['name_id']!r})")
            return title
    raise Error(f"missing patch definition: {name!r}")


def find_software_title(jss, name, details=True):
    """
    :param jss:         JSS API object
    :param name:        name of software title
    :param details:     if False, return simple (id + name) (default: True)

    :returns:           patch software title information
    """
    logger = logging.getLogger(__name__)
    logger.info(f"looking for existing software title: {name}")
    # Iterate all Patch Management Titles for specified matching name
    data = jss.get('patchsoftwaretitles')['patch_software_titles']
    for title in data['patch_software_title']:
        if title['name'] == name:
            logger.debug(f"found title: {name!r}")
            if details:
                logger.debug("returning detailed title info")
                jssid = title['id']
                return jss.get(f"patchsoftwaretitles/id/{jssid}")
            else:
                logger.debug("returning simple title info")
                return title
    raise Error(f"missing software title: {name!r}")


def new_softwaretitle(jss, name, category=None, source=jamf.KINOBI):
    """
    :param jss:         JSS API object
    :param name:        name of software title
    :param category:    dict of category to assign new title (id &| name)
    :param source:      source ID of external patch server 
                            (default: jamf.KINOBI) 

    :returns:           newly created patch software title
    """
    logger = logging.getLogger(__name__)
    logger.info(f"creating new software title: {name}")

    patch = find_patch_definition(jss, name, source)
    template = {'patch_software_title': {'name': name,
                                         'name_id': patch['name_id'],
                                         'source_id': source}}
    # assign category (if specified)
    if category:
        template['patch_software_title']['category'] = category

    logger.debug(f"template: {template!r}")
    new = jss.post('patchsoftwaretitles/id/0', template)
    # ID of newly created Patch Software Title
    jssid = new['patch_software_title']['id']
    logger.debug(f"created software title: {name!r} (ID:{jssid})")
    return jss.get(f"patchsoftwaretitles/id/{jssid}")


def update_softwaretitle_packages(jss, jssid, pkgs):
    """
    Update packages of software title
    
    :param jssid:        Patch Software Title ID
    :param pkgs:         dict of {version: package, ...}

    :returns: None
    """
    # TO-DO: Additional error handling

    logger = logging.getLogger(__name__)

    data = jss.get(f"patchsoftwaretitles/id/{jssid}")
    title = data['patch_software_title']

    name = title['name']
    logger.info(f"updating patch software title: {jssid} ({name})")
    
    # single version (dict), multiple versions (list)
    version = title['versions']['version']
    _modified = False
    try:
        # access key of single version and count on TypeError being raised
        v = version['software_version']
        if v in pkgs.keys():
            version['package'] = {'name': pkgs[v]}
            _modified = True

    except TypeError:
        # looks like it was actually a list
        for _version in version:
            v = _version['software_version']
            if v in pkgs.keys():
                _version['package'] = {'name': pkgs[v]}
                _modified = True

    if _modified:  
        result = jss.put(f"patchsoftwaretitles/id/{jssid}", data)
        logger.info(f"succesfully updated: {name}")
        return data
    else:
        logger.info(f"software title was not modified")


def create_patch_policies(jss, jssid, appname, stable, beta=None, latest=None):
    """
    Create new Patch Policies from template with existing SoftwareTitle

    :param jss:      jamf.API object
    :param jssid:    Patch Software Title ID
    :param appname:  name of application
    :param stable:   stable version number
    
    Optional:
        :param beta:     Guinea Pig version number (default: stable)
        :param alpha:    Tech version number (default: beta)
    """
    # Get icon from existing Policy with same name as Patch Policy
    policy = jss.get(f"policies/name/{appname}")
    icon_id = policy['policy']['self_service']['self_service_icon']['id']
    
    # Group ID's of Staging Smart Groups
    scoping = {'Tech - Test Boxes': {'id': 231},
               'Tech - Main Boxes': {'id': 230},
               'Guinea Pig - Lab': {'id': 171},
               'Guinea Pig - Staff': {'id': 229},
               'Stable - Lab': {'id': 234},
               'Stable - Staff': {'id': 233},
               # Experimental
               'Tech': [{'id': 231}, {'id': 230}],
               'Guinea Pig': [{'id': 171}, {'id': 229}],
               'Stable': [{'id': 234}, {'id': 233}]}
    
    # Use stable version if not otherwise stated
    beta = beta or stable
    latest = latest or beta

    # get patch template dictionaries
    templates = patch_templates(appname)
    # update template versioning 
    for t in templates:
        _name = t['name']
        if _name.startswith('Tech'):
            t['version'] = latest
        elif _name.startswith('Guinea Pig'):
            t['version'] = beta
        elif _name.startswith('Stable'):
            t['version'] = stable
    
    # Iterate each template
    for template in templates:
        name = template['name']
        method = template['method']
        
        # general settings
        general = {'name': f"{name} - {appname}",
                   'target_version': template['version'],
                   'enabled': True,
                   'distribution_method': method,
                   'allow_downgrade': False,
                   'patch_unknown': False}
        
        scope = {'computer_groups': {'computer_group': scoping[name]}}
        data = {'general': general, 'scope': scope}

        # Modify Self Service interaction (default: automatic)
        if method == 'selfservice':
            deferral = template.get('defer', 7)
            # user interaction settings
            interaction = {'self_service_icon': {'id': icon_id},
                           'deadlines': {'deadline_enabled': True,
                                         'deadline_period': deferral}}
            # notification settings
            # NOTE: I don't like this message, but if left blank becomes the 
            #       name of the patch policy (e.g. "Guinea Pig - Staff - app")
            msg = f"Update will automatically start in {deferral} days."
            n = {'notification_enabled': True,
                 'notification_type': 'Self Service',
                 'notification_subject': 'Update Available',
                 'notification_message': msg,
                 'reminders': {'notification_reminders_enabled': True,
                               'notification_reminder_frequency': 1}}
            interaction['notifications'] = n
            
            # grace period settings
            msg = ('$APP_NAMES will quit in 72 hours so'
                   ' that $SOFTWARE_TITLE can be updated. Save anything'
                   ' you are working on and quit the app(s)')
            g = {'grace_period_duration': 4320,
                 'notification_center_subject': 'Important',
                 'message': msg}
            interaction['grace_period'] = g
            
            # user interaction settings (default is automatic) 
            data['user_interaction'] = interaction
        
        # Post to JSS 
        endpoint = f"patchpolicies/softwaretitleconfig/id/{jssid}"
        jss.post(endpoint, {'patch_policy': data})


def verify_software_title(jss, _root_dict, category, pkgs):
    """
    verify software title
    """
    logger = logging.getLogger(__name__)
    logger.warning("software title verification incomplete")
    # root key: 'patch_software_title'
    title = _root_dict['patch_software_title']

    # clunky category check
    if title['category']['name'] != category['name']:
        logger.debug(f"software title: {title}")
        raise Error(f"invalid category: {category} != {title['category']}")
    
    # NOTE: this should check software packages, not modify them
    update_softwaretitle_packages(jss, title['id'], pkgs)




# EXPERIMENTAL

# def update_title_package(jss, name, version, pkg):
#     """
#     updates specified patch software title with the specified package
#     """
#     title = find_software_title(jss, name)
#     info = title['patch_software_title']
#     jssid = info['id']
#     target_ver = None
#     for v in info['versions']['version']:
#         if v['software_version'] == version:
#             v['package']['name'] = pkg
#             target_ver = v
#         
#     if not target_ver:
#         raise Error(f"invalid version: {version!r}:"
#                      " check definition and try again")
#     
#     data = {'patch_software_title': {'versions': {'version': target_ver}}}    
#     jss.put(f"patchsoftwaretitles/id/{jssid}", data)
  

# def update_title_package_rewrite(jss, name, ver, pkg):
#     """
#     rewritten update_title_package()
#     updates specified patch software title with the specified package
#     """
#     title = find_software_title(jss, name)
#     
#     # loop title for specified version
#     for v in title['patch_software_title']['versions']['version']:
#         if v['software_version'] == ver:
#             v['package']['name'] = pkg
#             version = v
# 
#     # build version modifications from root (excludes 
#     try:
#         mod = {'patch_software_title': {'versions': {'version': version}}}
#     except UnboundLocalError:
#         # if version isn't defined, it could not be found
#         raise Error(f"invalid version: {version!r}: "
#                      "check definition and try again")
# 
#     # build modifications from the root (will only modify the version)
#     mod = {'patch_software_title': {'versions': {'version': version}}}
#     jssid = title['patch_software_title']['id']
#     jss.put(f"patchsoftwaretitles/id/{jssid}", mod)



def patch_title(jss, name):
    """
    Experimental: patch object 
    """
    titles = jamf.patch.SoftwareTitles(jss)
    try:
        return titles.find(name)
    except jamf.patch.MissingTitleError:
        pass
    
    definitions = jamf.patch.AvailableTitles(jss, jamf.KINOBI)
    definition = definitions.find(name)
    return defintion


def patch_templates(name):
    """
    :returns: list of patch policy template dictionaries
    """
    global PATCH_TEMPLATES
    logger = logging.getLogger(__name__)
    logger.debug(f"getting policy template: {name!r}")
    return PATCH_TEMPLATES.get(name, DEFAULT_PATCH)


def update_patch_policy_version(jss, jssid, version):
    """
    Update Patch Policy version
    """
    logger = logging.getLogger(__name__)
    current = jss.get(f"patchpolicies/id/{jssid}")
    current_version = current['patch_policy']['general']['target_version']

    if current_version != version:
        name = current['patch_policy']['general']['name']
        logger.info(f"updating: {name!r}: {version}")
        data = {'patch_policy': {'general': {'target_version': version}}}
        jss.put(f"patchpolicies/id/{jssid}", data)


def update_softwaretitle_versions(jss, name, versions, pkgs=None):
    """
    Update all 
    :param jss:      JSS API object
    :param name:     name of external patch definition
    :param versions: {'Tech': version, 'Guinea Pig': version, 'Stable': version}

    :returns:
    """
    logger = logging.getLogger(__name__)
    jssid = find_software_title(jss, name, details=False)['id']

    if pkgs:
        update_softwaretitle_packages(jss, jssid, pkgs)

    for p in softwaretitle_policies(jss, jssid):
        # 'Tech - Test Boxes - Keynote' -> 'Tech'
        branch = p['name'].split(' - ')[0]
        try:
            update_patch_policy_version(jss, p['id'], versions[branch])
        except KeyError:
            logger.info(f"skipping: {p['name']!r}")
        
    
## ALL-IN-ONE

## ALL IN ONE FUNCTIONS  

def new_patch(jss, name, pkgs, version, beta=None, alpha=None):
    """
    Sets up new Patch Management Title
    - creates new patch software title
    - populates patch policies
    """
    logger = logging.getLogger(__name__)

    logger.debug(f"looking for policy: {name}")
    policy = jss.get(f"policies/name/{name}")['policy']
    # verify_policy(policy)
    # pprint.pprint(policy)
    
    # until better package system can be created
    if not isinstance(pkgs, dict):
        raise NotImplementedError(f"unsupported pkg type: {type(pkg)}")

    category = policy['general']['category']
    logger.debug(f"category: {name}")

    try:
        title = find_software_title(jss, name)
    except Error as e:
        logger.error(e)
        logger.info(f"creating new software title: {name}")
        title = new_softwaretitle(jss, name, category)

    verify_software_title(jss, title, category, pkgs)

    # create patch policies
    # 
    title_id = title['patch_software_title']['id']
    create_patch_policies(jss, title_id, name, version, beta, alpha)





if __name__ == '__main__':
    pass