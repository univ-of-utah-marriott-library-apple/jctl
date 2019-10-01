#!/usr/local/bin/python3

import jamf
import logging
import plistlib
import pprint

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



class Error(Exception):
    pass


def packages(jss, name=None):
    """
    returns packages matching name (case-insensitive)

    :param name <str>:  target name (i.e. name in d['name'])

    :returns:   list of dicts w/ keys: ('id', 'name')
                  e.g. [{'id': 23, 'name': 'vfuse-1.0.3.pkg'}, ...]
    """
    # return [pkg for pkg in packages if name in pkg['name']]
    name = name.lower()
    pkgs = []
    # for pkg in jss.get('packages', xml=True)['packages']['package']:
    for pkg in jss.get('packages')['packages']:
        if not name or name in pkg['name'].lower():
            pkgs.append(pkg)

    return pkgs


def package_details(jss, name=None):
    """
    :returns: detailed list of all packages in the JSS
    """
    # Each dict has the following keys:
    # ['allow_uninstalled',              # <bool> likely the index value (would be cool if it could be indexed via modification)
    #  'boot_volume_required',           # <bool> ? (universally: False)
    #  'category',                       # <str>  name of category
    #  'filename',                       # <str>  name of pkg file
    #  'fill_existing_users',            # <bool> ? (universally: False)
    #  'fill_user_template',             # <bool> ? (universally: False)
    #  'id',                             # <int>  JSS id
    #  'info',                           # <str>  contents of "Info" field
    #  'install_if_reported_available',  # <str>  ? (universally: 'false')
    #  'name',                           # <str>  name of package (typically same as filename)
    #  'notes',                          # <str>  contents of "Notes" field
    #  'os_requirements',                # <str>  os requirements? (universally: '')
    #  'priority',                       # <int>  installation priority? (universally: 10)
    #  'reboot_required',                # <bool> package requires reboot
    #  'reinstall_option',               # <str>  ? (universally: "Do Not Reinstall")
    #  'required_processor',             # <str>  processor limitation? (universally: 'None')
    #  'send_notification',              # <bool> ? (universally: False)
    #  'switch_with_package',            # <str>  ? (universally: 'Do Not Install')
    #  'triggering_files']               # <dict> ? (universally: {})

    # detailed list of every package (takes a long time)
    pkgs = []
    # isolating packages by name is handled by packages()
    for pkg in packages(jss, name):
        details = jss.get(f"packages/id/{pkg['id']}")
        pkgs.append(details['package'])
    return pkgs


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


def new_softwaretitle(jss, name, name_id, source_id=jamf.KINOBI):
    """
    Create new Patch Software Title
    
    :param name:        Display name of Patch Management Title
    :param name_id:     Unique name ID of external patch definition
    :param source_id:   External source id

    :returns: ID of newly created Patch Software Title 
    """
    # TO-DO: error handling
    # base template (had errors when populating packages and category)
    template = {'patch_software_title': {'name': name,
                                         'source_id': source_id, 
                                         'name_id': name_id}}

    new = jss.post('patchsoftwaretitles/id/0', template)
    return new['patch_software_title']['id']


def update_softwaretitle_packages(jss, jssid, pkgs):
    """
    Update packages of software title
    
    :param jssid:        Patch Software Title ID
    :param pkgs:         dict of {version: package, ...}
    :param category:     dict {'name': <category name>}

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

#     _modified = False
#     if isinstance(version, list):
#         for _version in version:
#             v = _version['software_version']
#             if v in pkgs.keys():
#                 _version['package'] = {'name': pkgs[v]}
#                 _modified = True
# 
#     elif isinstance(version, dict)
#         # update single version package
#         v = version['software_version']
#         if v in pkgs.keys():
#             version['package'] = {'name': pkgs[v]}
#             _modified = True

    if _modified:  
        jss.put(f"patchsoftwaretitles/id/{jssid}", data)
        logger.info(f"succesfully updated: {name}")
    else:
        logger.info(f"software title was not modified")
        

def find_software_title(jss, name):
    """
    :returns: patch software title by name
    """
    # list of all Patch Management Titles
    patch_titles = jss.get('patchsoftwaretitles')['patch_software_titles']
    for title in patch_titles:
        if title['name'] == name:
            jssid = title['id']
            return jss.get(f"patchsoftwaretitles/id/{jssid}", xml=True)
    
    # if nothing was found, raise error
    raise Error(f"unable to find software title: {name}")


def find_patch_policies(jss, name):
    """
    :returns: list of patch policies for Patch Software Title
    """
    # list of all Patch Management Titles
    patch_titles = jss.get('patchsoftwaretitles')['patch_software_titles']
    for title in patch_titles:
        if title['name'] == name:
            jssid = title['id']
            endpoint = f"patchpolicies/softwaretitleconfig/id/{jssid}"
            return jss.get(endpoint, xml=True)

    # if nothing was found, raise error
    raise Error(f"unable to find software title: {name}")
    

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


## MAIN

def main():
    address, auth = config('private/jss.plist')
    jss = jamf.JSS(address, auth=auth)
    
    # result = create_patch_policies(jss, 80, 'Seashore', '2.4.12')
    # pprint.pprint(result)
    
    # curl -s -H "authorization: Basic ${credentials}" -X "POST" -F name=@"path/to/the/icons/folder/${icons}" "${jps}/JSSResource/fileuploads/policies/id/${policy_id}"
    # curl -s -H "authorization: Basic YXBpc2FtOkxldHNzZWV3aGF0dGhpc2JhYnljYW5kbwo=" -X "POST" -F name=@"calibre.png" "https://casper.scl.utah.edu:8443/JSSResource/fileuploads/policies/id/440"
    
    ## requirements
    #   - Existing Patch Software Title
    #   - Existing Application Policy
    #   - Existing Version (w/ package)
        
    # TO-DO:
    # find existing software title
    #   Software Titles ('patchsoftwaretitles')
    #     patch_titles = jamf.patch.software(jss)
    #     patch_titles.find(appname)
    #  - availabletitles ('patchavailabletitles/sourceid/2')
    #     definitions = jamf.patch.definitions(jss) (jss.patch.definitions())
    #     definitions.find(appname)
    # Create Patch Software Title (if missing)
    #   - category
    #   - application policy
    #   - definition
       

if __name__ == '__main__':
    fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    main()