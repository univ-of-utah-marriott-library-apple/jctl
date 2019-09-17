#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jamf
import logging
import plistlib
import pprint

# goal: 9/3
# updates list of patch polices with given dictionary
# "Tech - Main Boxes" : {user_interaction}

def dump_object(obj):
    _data = {}
    for k in dir(obj):
        data[k] = getattr(obj, k)
    return _data


def patch_policies(jss):
    """
    :returns: list of all patch policies 
    """
    jss.get('patchpolicies')['patch_policies']

def patch_get_test(jss):
    patchsoftware = jss.get('patchsoftwaretitles')
    _id = None
    for title in patchsoftware['patch_software_titles']:
        if title['name'] == 'Trello':
            _id = title['id']
    
    patch = jss.get(f"patchpolicies/softwaretitleconfig/id/{_id}")
    for policy in patch['patch policies']:
        _id = policy['id']
        result = jss.get(f"patchpolicies/id/{_id}")
        pprint(result)
        print("-"*80)


STAFF = {'user_interaction': {'deadlines': {'deadline_enabled': True,
                                   'deadline_period': 7},
                     'grace_period': {'grace_period_duration': 4320,
                                      'message': ('$APP_NAMES will quit in 72 hours '
                                                  'so $SOFTWARE_TITLE can be updated. '
                                                  'Save your work and quit the app(s).'),
                                      'notification_center_subject': 'Important'},
                                      'install_button_text': 'Update',
                                      'notifications': {'notification_enabled': True,
                                                        'notification_subject': 'Update Available',
                                                        'notification_message': 'Update will automatically start in 7 days.',
                                                        'notification_type': 'Self Service',
                                       'reminders': {'notification_reminder_frequency': 1,
                                                     'notification_reminders_enabled': True}}}}

LAB = {
    'user_interaction': {
            'grace_period': {
                'grace_period_duration': 15,
                'message': '$APP_NAMES will quit in $DELAY_MINUTES minutes so '
                           'that $SOFTWARE_TITLE can be updated. Save anything '
                           'you are working on and quit the app(s)',
                'notification_center_subject': 'Important'}}}


def list_patchpolicies(jss, search=''):
    patchpolices = jss.get('patchpolicies')['patch_policies']
    return [p for p in patchpolices if search in p['name']]


def example_self_service(jss):
    policy = jss.get('patchpolicies/id/12')
    pprint.pprint(policy)


def update_patch_polices_named(jss, name, data):
    """
    applies data to all patch policies matching name
    :param jss:     JSS instance
    :param name:    limit updates to patch polices with name in string 
    :param data:    dictionary of values applied to each patch policy
    """
    policies = list_patchpolicies(jss, name)
    for policy in policies:
        jssid = policy['id']
        jss.put(f"patchpolicies/id/{jssid}", data)


def kinobi_definitions(jss, name=None):
    result = jss.get(f"patchavailabletitles/sourceid/2")
    jss.session.headers.update({'Accept': 'application/xml'})
    pprint.pprint(result)
    raise SystemExit()
    titles = result['patch_available_titles']['available_titles']
    if not name:
        return titles
    else:
        return [x for x in titles if x['app_name'] == name]


def software_titles(jss):
    result = jss.get('patchsoftwaretitles')
    titles = result['patch_software_titles']
    return titles


def create_patch_policy(jss, softwaretitleid, data):
    endpoint = f"patchpolicies/softwaretitleconfig/id/{softwaretitleid}"
    jss.post(endpoint, data)


def policy(jss, name):
    return jss.get(f"/policies/name/{name}")    


# idea
class PatchPolicy(object):
    """
    base class for JSS Patch Policies
    """
    pass


class AutomaticPatch(PatchPolicy):
    """
    class for automatic Patch Policies
    """
    pass


class InteractivePatch(PatchPolicy):
    """
    class for Patch Policies available in Self Service
    """
    pass


class Policy(object):

    def __init__(self, name=None, jssid=None):
        self._name = name
        self._jssid = jssid
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, string):
        raise NotImplementedError()


class AppPolicy(Policy):
    """
    specialized Policy for applications
    """
    def __init__(self, name):
        pass


def update_patch_management(jss, jssid, policy, ver, pkg):
    """
    updates existing patch management
    """
    raise NotImplementedError()
    

def create_patch_policies(jss, titleID, appname, stable, beta=None, latest=None):
    """
    Create new Patch Policies from template with existing SoftwareTitle
    """
    policy = jss.get(f"policies/name/{appname}")
    # pprint.pprint(policy)
    # raise SystemExit()
    icon_id = policy['policy']['self_service']['self_service_icon']['id']
    
    scoping = {'Tech - Test Boxes': {'id': 231},
               'Tech - Main Boxes': {'id': 230},
               'Guinea Pig - Lab': {'id': 171},
               'Guinea Pig - Staff': {'id': 229},
               'Stable - Lab': {'id': 234},
               'Stable - Staff': {'id': 233}}
    
    beta = beta or stable
    latest = latest or beta

    # policy templates
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

    for template in templates:
        name = template['name']

        # general
        general = {'name': f"{name} - {appname}",
                   'target_version': template['version'],
                   'enabled': True,
                   'distribution_method': template['method'],
                   'allow_downgrade': False,
                   'patch_unknown': False}

        # scoping
        scope_id = scoping[name]
        scope = {'computer_groups':{'computer_group':{'id':scope_id}}}

        data = {'general': general, 'scope': scope}
        
        # Dynamic Notification
        if ('Main' in name) or ('Staff' in name):                        
            deferral = policy.get('defer', 7)

            # I don't like this message, but if left blank becomes
            # the name of the patch policy (e.g. "Guinea Pig - Staff - app")
            msg = f"Update will automatically start in {deferral} days."

            notify = {'notification_enabled': True,
                      'notification_type': 'Self Service',
                      'notification_subject': 'Update Available',
                      'notification_message': msg,
                      'reminders': {'notification_reminders_enabled': True,
                                    'notification_reminder_frequency': 1},
                      'deadlines': {'deadline_enabled': True,
                                    'deadline_period': deferral}}

            interaction = {'notifications': notify,
                           # 'install_button_text': 'Update',
                           'self_service_icon': {'id': icon_id},
                           'deadlines': {'deadline_enabled': True,
                                         'deadline_period': deferral}}
            
            # set the grace_period if modified (otherwise uses default)
            grace = {'grace_period_duration': 4320,
                     'notification_center_subject': 'Important',
                     'message': ('$APP_NAMES will quit in 72 hours so'
                                 ' that $SOFTWARE_TITLE can be updated. Save anything'
                                 ' you are working on and quit the app(s)')}

            interaction['grace_period'] = grace
            
            data['user_interaction'] = interaction
        
        endpoint = f"patchpolicies/softwaretitleconfig/id/{titleID}"
        jss.post(endpoint, {'patch_policy': data})


def main():
    config = plistlib.readPlist('private/jss')
    auth = config['login'].split(':')
    address = config['address']
    jss = jamf.JSS(address, auth=auth)
    
    ## Used to create new patch policies for existing SoftwareTitle()
    # create_patch_policies(jss, 77, 'NVivo', '12.2.0')
    

    ## patch.SoftwareTitles()
    # titles = jamf.patch.SoftwareTitles(jss)
    # pprint.pprint(titles.titles)
    
    ## looks for Patch Software Title with specified name
    # result = titles.find('Google Chrome')
    # pprint.pprint(result)

        

if __name__ == '__main__':
    fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    main()
    
