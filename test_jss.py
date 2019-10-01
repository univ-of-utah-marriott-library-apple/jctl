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
                              

class Error(Exception):
    pass


## SIMPLE FUNCTIONS

def patch_policies(jss):
    """
    :returns: list of all patch policies 
    """
    return jss.get('patchpolicies')['patch_policies']


def all_packages(jss):
    """
    :returns: list of dictionaries for all packages on JSS
    """
    # Each entry is dict containing the following keys:
    # ['id',     # <int>  JSS id
    #  'name']   # <str> name of package
    # return jss.get('packages', xml=True)['packages']['package']
    return jss.get('packages')['packages']


def policy(jss, name):
    return jss.get(f"/policies/name/{name}")    


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


## replaced with 'find_patch_definition()'
# def kinobi_definitions(jss, name=None):
#     """
#     :param name:  if specified, only returns patch defintion with name
#     :returns: 
#     """
#     endpoint = f"patchavailabletitles/sourceid/{jamf.KINOBI}"
#     result = jss.get(endpoint, xml=True)['patch_available_titles']
#     titles = result['available_titles']['available_title']
# 
#     if not name:
#         return titles
#     else:
#         return [x for x in titles if x['app_name'] == name]


def find_patch_definition(jss, name, source=jamf.KINOBI):
    logger = logging.getLogger(__name__)
    logger.info(f"looking for definition: {name!r} (source: {source})")
    endpoint = f"patchavailabletitles/sourceid/{source}"
    result = jss.get(endpoint, xml=True)['patch_available_titles']
    all_titles = result['available_titles']['available_title']
    for title in all_titles:
        if name == title['app_name']:
            logger.debug(f"found definition: {title['name_id']})")
            return title
    raise Error(f"missing patch definition: {name!r}")


def find_software_title(jss, name, details=True):
    """
    :returns: patch software title by name
    """
    # Iterate all Patch Management Titles for specified matching name
    data = jss.get('patchsoftwaretitles', xml=True)['patch_software_titles']
    for title in data['patch_software_title']:
        if title['name'] == name:
            if details:
                jssid = title['id']
                return jss.get(f"patchsoftwaretitles/id/{jssid}", xml=True)
            else:
                return title
    raise Error(f"missing software title: {name!r}")


# def create_patch_policies_draft(jss, appname):
#     """
#     create patch policies from existing policy
#     """
#     # look for existing policy
#     policy = jss.get(f"policies/name/{appname}", xml=True)['policy']
#     general = policy['general']
#     jssid = general['id']
#     category = general['category']
#     pkg = policy['package_configuration']['packages']['package']
#     packages = policy['package_configuration']['packages']
#     
#     # NOTE: this is underdeveloped garbage
#     if int(packages['size']) != 1:
#         for pkg in packages['package']:
#             # {'id': pkg['id'], 'name': pkg['name']}
#             pass
#     else:
#         # small subset
#         pkg = {k:v for k,v in packages['package'] if k in ('id', 'name')}


def new_softwaretitle(jss, name, category, source=jamf.KINOBI):

    logger = logging.getLogger(__name__)
    logger.info(f"creating new software title: {name}")

    patch = find_patch_definition(jss, name)
    template = {'patch_software_title': {'name': name,
                                         'name_id': patch['name_id'],
                                         'source_id': source,
                                         'category': category}}
    logger.debug(f"template: {template!r}")
    new = jss.post('patchsoftwaretitles/id/0', template)
    # JSS ID of newly created Patch Software Title
    jssid = new['patch_software_title']['id']
    logger.info(f"successfully created software title: {name} (ID: {jssid})")
    return jss.get(f"patchsoftwaretitles/id/{jssid}", xml=True)


# def new_softwaretitle_old(jss, name, name_id, source_id=jamf.KINOBI):
#     """
#     Create new Patch Software Title
#     
#     :param name:        Display name of Patch Management Title
#     :param name_id:     Unique name ID of external patch definition
#     :param source_id:   External source id
# 
#     :returns: ID of newly created Patch Software Title 
#     """
#     # TO-DO: error handling
#     # base template (had errors when populating packages and category)
#     template = {'patch_software_title': {'name': name,
#                                          'source_id': source_id, 
#                                          'name_id': name_id}}
# 
#     new = jss.post('patchsoftwaretitles/id/0', template)
#     return new['patch_software_title']['id']


def update_softwaretitle_packages(jss, jssid, pkgs):
    """
    Update packages of software title
    
    :param jssid:        Patch Software Title ID
    :param pkgs:         dict of {version: package, ...}

    :returns: None
    """
    # TO-DO: Additional error handling

    logger = logging.getLogger(__name__)

    data = jss.get(f"patchsoftwaretitles/id/{jssid}", xml=True)
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
               'Stable - Staff': {'id': 233}}
    
    # Use stable version if not otherwise stated
    beta = beta or stable
    latest = latest or beta

    # Policy Templates
    #  Tech (test + main)
    #  Guinea Pig (lab + staff)
    #  Stable (lab + staff)
    templates = [
                {'name': 'Tech - Test Boxes',
                 'version': latest,
                 'method': 'prompt'},
                {'name': 'Tech - Main Boxes',
                 'defer': 2,
                 'version': latest,
                 'method': 'selfservice'},
                {'name': 'Guinea Pig - Lab',
                 'version': beta,
                 'method': 'prompt'},
                {'name': 'Guinea Pig - Staff',
                 'version': beta,
                 'method': 'selfservice'},
                {'name': 'Stable - Lab',
                 'version': stable,
                 'method': 'prompt'},
                {'name': 'Stable - Staff',
                 'version': stable,
                 'method': 'selfservice'}
                ]
    
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
        
        # scoping settings
        scope_id = scoping[name]
        scope = {'computer_groups': {'computer_group': {'id': scope_id}}}
        
        data = {'general': general, 'scope': scope}
        
        # Modify Self Service interaction (default: automatic)
        if method == 'selfservice':
            deferral = policy.get('defer', 7)
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


def app_policy(jss, name, template=None):
    """
    checks for existing app policy
    """
    all_policies = jss.get('policies')
    pprint.pprint(all_policies)


def test_policy_modification(jss, jssid, icon):
    """
    Verify setting some values adjust others
    """
    existing = jss.get(f"policies/id/{jssid}", xml=True)['policy']

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
    result = jss.get('policies/id/453', xml=True)
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

def config(plist):
    """
    loads configuration from plist
    :returns: address, (username, passwd)
    """
    with open(plist, 'rb') as f:
        c = plistlib.load(f)
    user, passwd = c['login'].split(':')
    return c['address'], (user, passwd)


def dump_object(obj):
    _data = {}
    for k in dir(obj):
        data[k] = getattr(obj, k)
    return _data


def api():
    import plistlib
    import jamf
    config = plistlib.readPlist('private/jss.plist')
    auth = config['login'].split(':')
    address = config['address']
    return jamf.JSS(address, auth=auth)


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

        
def new_management_title_workflow(jss):
    """
    works for creating new patches
    """
#     name = 'calibre'
#     pkgs = {'3.47.1': 'calibre_3.47.1_2019.09.04_rcg.pkg',
#             '3.48.0': 'calibre_3.48.0_2019.09.19_rcg.pkg'}
#     new_patch(jss, name, pkgs, '3.47.1', '3.48.0')

#     name = 'MuseScore 3'
#     pkgs = {'3.2.3': 'musescore_3_3.2.3.22971_2019.09.04_rcg.pkg'}
#     new_patch(jss, name, pkgs, '3.2.3')

#     name = 'Mendeley Desktop'
#     pkgs = {'1.19.4': 'mendeley_desktop_1.19.4_2019.09.04_rcg.pkg'}
#     new_patch(jss, name, pkgs, '1.19.4')

#     name = 'ATLAS.ti'
#     pkgs = {'8.4.4': 'atlas_8.4.4_2019.09.17_rcg.pkg'}
#     new_patch(jss, name, pkgs, '8.4.4')


## MAIN

def main():
    address, auth = config('private/jss.plist')
    jss = jamf.JSS(address, auth=auth)
        
    ## clunky all in one patch creation 
    #  - requires existing app policy
    #  - does not gracefully handle pre-existing patch-policies
    # appname = None
    # pkgs = {}
    # all_in_one_patch(jss, appname)



if __name__ == '__main__':
    fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    main()
    
