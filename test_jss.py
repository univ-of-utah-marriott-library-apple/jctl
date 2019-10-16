#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
various functions for building jamf library
"""

import logging
import plistlib
import pprint
import os

import jamf

#NOTE: this should be imported externally
# TO-DO:
    # Policy Updating
    # - description testing
    # - report blank descriptions
    # - parse and add version               

    # Patch Policy Version Updates

    # Package workflows               


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
    

def update_all_patch_policies(api, template):
    """
    :param template:  fully qualified dict of global patch modification
                      {'patch_policy': {'general': {'patch_unknown': 'false'}}}
    :returns None:
    """
    
    for p in patch.patch_policies(api):
        api.put(f"patchpolicies/id/{p['id']}", template)
    

def update_patch_policies(api, name, versions, pkgs):
    """
    :param api:   jamf.API object
    :param name:  name of software title
    """
    raise NotImplementedError("verify the changes first")

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
    api = jamf.API(address, auth=auth)
    # p = jamf.policy.update_app_policy(api, 468, {'id': 285, 'name': 'tweetdeck_3.16.1_2019.09.18_rcg.pkg', 'action': 'Install'})
    # pprint.pprint(p)
    jamf.patch.create_patch_policies(api, 26, 'VueScan', '9.7.04')


if __name__ == '__main__':
    fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    main()
    
