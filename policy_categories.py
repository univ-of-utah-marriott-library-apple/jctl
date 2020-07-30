#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Policy Categories

This script allows you to change the categories of all of your polices at once.
You must know a little bit of Python to use this script. This script will not
add categories. Use the GUI for that.

This script isn't standard by any measure. Running this script will generate a
list of categories and the polices. Here's an example of what it would print.

mass_edit = {
    'Admin': [
    ],
    'Utilities': [
        'Install RadmindTools',
    ],
}

Sooo... basically if you want change the category of the Install RadmindTools
policy you need to cut it out of the Utilities array and paste it into the
Admin array, and here's where it gets non-standard, *copy* the code and *paste*
it into this script. That's right, edit this script. Then run this script
again. Magic.

To get it to display all of your categories and policies again, just make sure
you have the following variable empty.

mass_edit = {}

Remember, this script will not add categories.
"""

__author__ = 'James Reynolds'
__email__ = 'reynolds@biology.utah.edu'
__copyright__ = 'Copyright (c) 2020, The University of Utah'
__license__ = 'MIT'
__version__ = "1.0.4"


import jamf


mass_edit = {
}

jss = jamf.API()
temp_categories = jss.get('categories')['categories']['category']
categories = {ii['name']: ii['id'] for ii in temp_categories}
categories['No category assigned'] = -1
temp_policies = jss.get('policies')['policies']['policy']
policies = {ii['name']: ii['id'] for ii in temp_policies}

if len(mass_edit) == 0:
    for policy_name in policies:
        policy_id = policies[policy_name]
        policy = jss.get(f"policies/id/{policy_id}")
        policy_category_name = policy['policy']['general']['category']['name']
        if policy_category_name not in mass_edit:
            mass_edit[policy_category_name] = []
        mass_edit[policy_category_name].append(policy_name)
    print("mass_edit = {")
    for category in categories:
        print(f"    '{category}': [")
        if category in mass_edit:
            for policy_name in mass_edit[category]:
                print(f"        '{policy_name}',")
        print("    ],")
    print("}")
else:
    for category_name in mass_edit:
        policy_arr = mass_edit[category_name]
        if category_name in categories:
            for policy_name in policy_arr:
                if policy_name in policies:
                    policy_id = policies[policy_name]

                    print(f"Working on {policy_name}")
                    policy = jss.get(f"policies/id/{policy_id}")
                    category_dict = {'id': categories[category_name],
                                     'name': category_name}
                    policy['policy']['general']['category'] = category_dict
                    jss.put(f"policies/id/{policy_id}", policy)
                else:
                    print(f"ERROR: Policy \"{policy_name}\" is missing")
        else:
            print(f"ERROR: Category \"{category_name}\" is missing")
