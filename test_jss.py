#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jamf
import logging
import plistlib
import pprint
import os

## GLOBALS

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
## TO-DO:
    # Policy Updating
    # - description testing
    # - report blank descriptions
    # - parse and add version               

    # Patch Policy Version Updates

    # Package workflows               

class Error(Exception):
    pass


## SIMPLE FUNCTIONS

def patch_policies(jss, name=None):
    """
    :returns: list of all patch policies 
    """
    policies = jss.get('patchpolicies')['patch_policies']['patch_policy']
    if name is not None:
        return [x for x in policies if name in x['name']]
    else:
        return policies


def packages(jss):
    """
    :returns: list of dictionaries for all packages on JSS
    """
    # Each entry is dict containing the following keys:
    # ['id',     # <int>  JSS id
    #  'name']   # <str> name of package
    # return jss.get('packages')['packages']['package']
    return jss.get('packages')['packages']


## EXPERIMENTAL

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


def find_patch_definition(jss, name, source=jamf.KINOBI):
    """
    :param jss:     JSS API object
    :param name:    name of external patch definition
    :param source:  source ID of external patch server (default: jamf.KINOBI) 

    :returns:       external patch definition by name
    """
    logger = logging.getLogger(__name__)
    logger.info(f"looking for external definition: {name!r}")
    logger.debug(f"patch source ID: {source}")
    endpoint = f"patchavailabletitles/sourceid/{source}"
    result = jss.get(endpoint)['patch_available_titles']
    all_titles = result['available_titles']['available_title']
    for title in all_titles:
        if name == title['app_name']:
            logger.debug(f"found definition ID: {title['name_id']!r})")
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


def patch_templates(name):
    """
    :returns: list of patch policy template dictionaries
    """
    global PATCH_TEMPLATES
    logger = logging.getLogger(__name__)
    logger.debug(f"getting policy template: {name!r}")
    return PATCH_TEMPLATES.get(name, DEFAULT_PATCH)


def new_patch_policy(jss, jssid, name, scope, version, interaction=None):
    """
    This already seems like a bad idea...
    
    not enough can be derived for this function to properly build a post
    dynamically while still being useful enough
    
    """
    # a better approach might be to have a function return a populated 
    # template and then simply call
    # jss.post(endpoint, template)
    pass


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
        
    
def softwaretitle_policies(jss, jssid):
    """
    :returns: list of software title patch policies
    """
    endpoint = f"patchpolicies/softwaretitleconfig/id/{jssid}"
    return jss.get(endpoint)['patch_policies']['patch_policy']


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

## HERE

def new_app_policy(jss, name):
    """
    workflow of creating a new app policy
    """
    # questions:
    # what does a base-minimum new policy look like?
    raise NotImplementedError("not yet finished")
    all_policies = jss.get('policies')
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


def all_app_policies(jss, name, template=None):
    """
    
    """
    all_policies = jss.get('policies')
    pprint.pprint(all_policies)


def test_policy_modification(jss, jssid, icon):
    """
    Verify setting some values adjust others
    """
    existing = jss.get(f"policies/id/{jssid}")['policy']

    # upload icon if it's missing
    if not existing['self_service']['self_service_icon']:
        jss.upload(f"policies/id/{jssid}", icon)
    
    category = CATEGORY['Apps - Office']
    policy = {'general': {'category': category},
              'self_service': {
                'self_service_categories': {'category': category}}
              }
    result = jss.put('policies/id/453', {'policy': policy})
    pprint.pprint(result)


def new_policy_workflow(jss):
    name = 'OmniFocus'
    icon = 'OmniFocus.png'
    package = None
    category = None
    template = None
    timestamp = None
    
    # create_app_policy(jss, name)
    # template = app_policy_template(name)
    # result = jss.post('policies/id/0', template)
    # pprint.pprint(result)
    result = jss.get('policies/id/453')
    return result



## VERIFICATION

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


def verify_policy(policy):
    """
    verify policy
    """
    logger = logging.getLogger(__name__)
    logger.warning("policy verification incomplete")
    # raise NotImplementedError("not finished")


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




## HELPER FUNCTIONS

def dump_object(obj):
    _data = {}
    for k in dir(obj):
        data[k] = getattr(obj, k)
    return _data


def config(plist):
    """
    loads configuration from plist
    :returns: address, (username, passwd)
    """
    with open(plist, 'rb') as f:
        c = plistlib.load(f)
    user, passwd = c['login'].split(':')
    return c['address'], (user, passwd)


def installer_packages():
    """
    quick and dirty dump of packages on InstallerPackages
    """
    vol = '/Volumes/InstallerPackages/munkipkg_projects'
    import glob
    g = os.path.join(vol, '*/payload/*.app')
    info = {}
    for path in glob.glob(g):
        name = os.path.splitext(os.path.basename(path))[0]
        directory = path.split('/payload')[0]
        folder = os.path.basename(directory)
        pkgs = []
        for pkg in glob.glob(os.path.join(directory, 'build/*.pkg')):
            pkgs.append(os.path.basename(pkg))

        plist = os.path.join(directory, 'build-info.plist')
        with open(plist, 'rb') as f:
            b_info = plistlib.load(f)

        info[name] = {'pkgs': pkgs, 'folder': folder, 
                      'build': b_info, 'name': name}
    
    pprint.pprint(info)

        
def new_management_title_workflow_example(jss):
    """
    works for creating new patches
    """
    # name = 'calibre'
    # pkgs = {'3.47.1': 'calibre_3.47.1_2019.09.04_rcg.pkg',
    #         '3.48.0': 'calibre_3.48.0_2019.09.19_rcg.pkg'}
    # new_patch(jss, name, pkgs, '3.47.1', '3.48.0')
    # 
    # name = 'MuseScore 3'
    # pkgs = {'3.2.3': 'musescore_3_3.2.3.22971_2019.09.04_rcg.pkg'}
    # new_patch(jss, name, pkgs, '3.2.3')
    # 
    # name = 'Mendeley Desktop'
    # pkgs = {'1.19.4': 'mendeley_desktop_1.19.4_2019.09.04_rcg.pkg'}
    # new_patch(jss, name, pkgs, '1.19.4')
    # 
    # name = 'ATLAS.ti'
    # pkgs = {'8.4.4': 'atlas_8.4.4_2019.09.17_rcg.pkg'}
    # new_patch(jss, name, pkgs, '8.4.4')
    # 
    # name = 'Evernote'
    # pkgs = {'7.13': 'evernote_7.13_2019.09.24_rcg.pkg'}
    # new_patch(jss, name, pkgs, '7.13')
    #
    # name = 'Scratch Desktop'
    # pkgs = {'3.6.0': 'scratch_desktop_3.6.0_2019.09.27_rcg.pkg'}
    # new_patch(jss, name, pkgs, '3.6.0')
    # 
    # name = 'Final Cut Pro'
    # pkgs = {'10.4.6': 'final_cut_pro_10.4.6_2019.09.20_rcg.pkg'}
    # new_patch(jss, name, pkgs, '10.4.6')
    # 
    # name = 'Motion'
    # pkgs = {'5.4.3': 'motion_5.4.3_2019.09.20_rcg.pkg'}
    # new_patch(jss, name, pkgs, '5.4.3')
    # 
    # name = 'Camtasia 3'
    # pkgs = {'3.1.5': 'camtasia_3_3.1.5_2019.09.20_rcg.pkg'}
    # new_patch(jss, name, pkgs, '3.1.5')
    # 
    # name = 'OmniFocus'
    # pkgs = {'3.4.2': 'omnifocus_3.4.2_2019.09.19_rcg.pkg'}
    # new_patch(jss, name, pkgs, '3.4.2')

    # name = 'StatPlus'
    # version = '7.0.1.0'
    # pkgs = {version: 'statplus_7.0.1.0_2019.09.30_rcg.pkg'}
    # new_patch(jss, name, pkgs, version)

    # name = 'SubEthaEdit'
    # version = '5.1'
    # pkgs = {version: 'subethaedit_5.1_2019.09.24_rcg.pkg'}
    # new_patch(jss, name, pkgs, version)

    # 2019.10.09

    # name = '1Password 7'
    # version = '7.3.2'
    # pkgs = {version: '1password_7_7.3.2_2019.10.07_rcg.pkg'}
    # new_patch(jss, name, pkgs, version)

    # name = 'PDF Squeezer'
    # version = '3.10.5'
    # pkgs = {version: 'pdf_squeezer_3.10.5_2019.10.08_rcg.pkg'}
    # new_patch(jss, name, pkgs, version)

    # name = 'GarageBand'
    # version = '10.3.2'
    # pkgs = {version: 'garageband_10.3.2_2019.08.29_rcg.pkg'}
    # new_patch(jss, name, pkgs, version)
    
    # name = 'Sequel Pro'
    # version = '1.1.2'
    # pkgs = {version: 'sequel_pro_1.1.2_2019.10.03_rcg.pkg'}
    # new_patch(jss, name, pkgs, version)

    # name = 'MovieCaptioner'
    # version = '6.5.0'
    # pkgs = {version: 'moviecaptioner_6.5.0_2019.10.08_rcg.pkg'}
    # new_patch(jss, name, pkgs, version)

    # name = 'Screenflick'
    # version = '2.7.43'
    # pkgs = {version: 'screenflick_2.7.43_2019.10.08_rcg.pkg'}
    # new_patch(jss, name, pkgs, version)

    pass
    

def update_all_patch_policies(jss):
    # result = jss.get('patchpolicies/id/79')
    mod = {'patch_policy': {'general': {'patch_unknown': 'false'}}}
    
    for p in patch_policies(jss):
        jss.put(f"patchpolicies/id/{p['id']}", mod)
    

def update_patch_policies(jss):

    pkgs = {}
    # name = 'Numbers'
    # versions = {'Tech': '6.2', 'Guinea Pig': '6.2', 'Stable': '6.2'}
    # pkgs = {'6.2': 'numbers_6.2_2019.10.01_rcg.pkg'}

    # name = 'Spark'
    # versions = {'Tech': '2.3.12', 'Guinea Pig': '2.3.12', 'Stable': '2.3.12'}
    # pkgs = {'2.3.12': 'spark_2.3.12_2019.10.01_rcg.pkg'}    

    # name = 'Keyboard Maestro'
    # versions = {'Tech': '9.0.2'}
    # pkgs = {'9.0.2': 'keyboard_maestro_9.0.2_2019.09.13_rcg.pkg',
    #         '9.0.1': 'keyboard_maestro_9.0.1_2019.08.30_rcg.pkg'}

    # name = 'LibreOffice'
    # versions = {'Tech': '6.3.2002', 'Guinea Pig': '6.3.2002', 'Stable': '6.3.2002'}
    # pkgs = {'6.3.2002': 'libreoffice_6.3.2002_2019.09.27_rcg.pkg'}    

    # name = 'Spotify'
    # versions = {'Tech': '1.1.15.448', 'Guinea Pig': '1.1.15.448', 'Stable': '1.1.15.448'}
    # pkgs = {'1.1.15.448': 'spotify_1.1.15.448.g00fba0e3-14_2019.09.20_rcg.pkg'}    

    # name = 'Tableu Public'
    # versions = {'Stable': '2019.3.0'}
    # versions = {'Tech': '2019.3.0', 'Guinea Pig': '2019.3.0', 'Stable': '2019.3.0'}
    # pkgs = {'2019.2.3': 'tableau_public_2019.2.3_2019.09.09_rcg.pkg',
    #         '2019.3.0': 'tableau_public_2019.3.0_2019.09.20_rcg.pkg'} 


    # 2019.10.08
    # name = 'Microsoft Remote Desktop'
    # versions = {'Tech': '10.3.3', 'Guinea Pig': '10.3.3', 'Stable': '10.3.2'}
    # pkgs = {'10.3.3': 'microsoft_remote_desktop_10.3.3_2019.10.08_rcg.pkg'} 

    # name = 'GarageBand'
    # versions = {'Tech': '10.3.3', 'Guinea Pig': '10.3.3', 'Stable': '10.3.2'}
    # pkgs = {'10.3.3': 'garageband_10.3.3_2019.10.08_rcg.pkg'} 

    # name = '1Password 7'
    # versions = {'Tech': '7.3.2', 'Guinea Pig': '7.3.2', 'Stable': '7.3.2'}
    # pkgs = {'7.3.2': '1password_7_7.3.2_2019.10.07_rcg.pkg'} 

    # name = 'Logic Pro X'
    # versions = {'Tech': '10.4.7', 'Guinea Pig': '10.4.7', 'Stable': '10.4.6'}
    # pkgs = {'10.4.6': 'logic_pro_x_10.4.6_2019.08.29_rcg.pkg',
    #         '10.4.7': 'logic_pro_x_10.4.7_2019.10.08_rcg.pkg'}
    
    # name = 'Cyberduck'
    # versions = {'Tech': '7.1.1', 'Guinea Pig': '7.1.0', 'Stable': '7.1.0'}
    # pkgs = {'7.1.1': 'cyberduck_7.1.1_2019.10.08_rcg.pkg'} 

    # name = 'Skype'
    # versions = {'Tech': '8.53', 'Guinea Pig': '8.53', 'Stable': '8.52'}
    # pkgs = {'8.53': 'skype_8.53.0.85_2019.10.08_rcg.pkg'} 

    # name = 'Opera'
    # versions = {'Tech': '64.0.3417.47', 'Guinea Pig': '63.0.3368.75', 'Stable': '63.0.3368.75'}
    # pkgs = {'64.0.3417.47': 'opera_64.0.3417.47_2019.10.08_rcg.pkg'} 

    # name = 'Motion'
    # versions = {'Tech': '5.4.4', 'Guinea Pig': '5.4.3', 'Stable': '5.4.3'}
    # pkgs = {'5.4.4': 'motion_5.4.4_2019.10.08_rcg.pkg'} 

    name = 'Dropbox'
    versions = {
        'Tech': '82.4.155', 
        'Guinea Pig': '82.4.155', 
        'Stable': '82.4.155'
    }
    pkgs = {'82.4.155': 'dropbox_82.4.155_2019.10.09_swf.pkg'}
    update_softwaretitle_versions(jss, name, versions, pkgs)
    pass
    

## MAIN

def main():
    address, auth = config('private/jss.plist')
    jss = jamf.API(address, auth=auth)
    
    # new_management_title_workflow_example(jss)
    update_patch_policies(jss)

    # global modifications of patch policies (disable unknown upgrades
    # update_all_patch_policies(jss)


if __name__ == '__main__':
    fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    main()
    
