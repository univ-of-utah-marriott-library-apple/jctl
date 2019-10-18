# -*- coding: utf-8 -*-

"""
Utility for creating templates 
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"

import os
import sys
import copy
import logging
import plistlib
import subprocess
import datetime as dt

# import jamf

TEMPLATES = '/path/to/templates'


class Error(Exception):
    pass


class Record(object):
    
    def __init__(self, path):
        self.log = logging.getLogger(f"{__name__}.Record")
        self.path = path
        self.data = {}
    
    def load(self):
        self.log.debug("loading: %r", self.path)
        with open(self.path, 'rb') as f:
            self.data = plistlib.load(f)
            return self.data
    
    def save(self, data=None):
        self.log.debug("saving: %r", self.path)
        _data = data or self.data
        with open(self.path, 'wb') as f:
            plistlib.dump(data, f)

    def update(self, key, data):
        self.log.debug("updating: %r", key)
        self.data.setdefault(key, {})
        self.data[key].update(data)

    def append(self, key, data):
        self.log.debug("appending: %r", key)
        self.data.setdefault(key, [])
        self.data[key].append(data)

    def merge(self, data):
        raise NotImplementedError()


def patch_policy_template(schema):
    """
    Construct patch policy creation instructions using schema
    :returns: patch policy instruction data
    """
    # interpret schema to construct a template for patch policy creation
    # TO-DO: this will have to be figured out
    raise NotImplementedError()


def template_from_policy(api, jssid, name):
    """
    Create template from existing policy
    """
    # get policy
    p = api.get(f"policies/id/{jssid}")
    
    # meta information
    info = {
        'name': name,       
        # 'icon': None,       # icon information?
        # 'version': None,    # jamf version?
    }
    
    # remove default policy info (not part of template) 
    _template = trim_policy(p['policy'])
    # _template = {}
    # get common key/values for all future policies
    # general
    #   category                # specific
    #   date_time_limitations
    #   frequency
    #   network_limitations
    #   network_requirements
    #   site
    #   trigger
    #   trigger_checkin
    #   trigger_enrollment_complete
    #   trigger_login
    #   trigger_logout
    #   trigger_network_state_changed
    #   trigger_other
    #   trigger_startup
    #   target_drive
    #   
    # scope
    #   all_computers
    #   buildings
    #   computer_groups
    #   computers
    #   departments
    #   exclusions
    #   limit_to_users
    #   limitations
    # 
    # self_service
    #   feature_on_main_page
    #   force_users_to_view_description
    #   install_button_text
    #   notification
    #   notification_message
    #   notification_subject
    #   reinstall_button_text
    #   self_service_description
    #   self_service_display_name
    #   self_service_icon
    #   use_for_self_service
    #   
    # scripts
    # user_interaction

    # save template
    info['template'] = _template
    return save_template(info)


def trim_policy(policy_data):
    """
    remove unique/default data from policy
    """
    unique = {'general': ('category', 'id', 'name'),
              # 'scripts': (),
              'self_service': ('notification_subject', 
                               'self_service_categories',
                               'self_service_description',
                               'self_service_display_name',
                               'self_service_icon')}
    excluded = ('account_maintenance', 'disk_encryption', 'dock_items', 
                'files_processes', 'maintenance', 'package_configuration',
                'printers', 'reboot')
    keys = ('general', 'scope', 'scripts', 'self_service', 'user_interaction')
    trimmed = {}
    for key in keys:
        for k, v in policy_data[key].items():
            if k not in unique.get(key, ()):
                info = trimmed.setdefault(key, {})
                info[k] = copy.deepcopy(v)
    return trimmed        

#     trimmed = copy.deepcopy(policy_data)
#     for k in excluded:
#         del(trimmed[k])
#     
#     for key in keys:
#         try:            
#             for k in unique[key]:
#                 del(trimmed[key][k])
#         except KeyError:
#             pass
#     return trimmed


def merge_templates(templates):
    """
    Produce single template from multiple ones
    """
    raise NotImplementedError()


def load_template(name):
    """
    Retrieve and load saved by name template
    """
    for n in os.listdir(TEMPLATES):
        if name in n:
            path = os.path.join(TEMPLATES, n)
            return Record(path).load()


def save_template(data, path=None):
    """
    write data to specified path
    """
    if not path:
        name = "{0!s}.plist".format(data['name'])
        path = os.path.join(TEMPLATES, name)
    Record(path).save(data)
    return path


def main():
    pass
    

if __name__ == '__main__':
    fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    main()