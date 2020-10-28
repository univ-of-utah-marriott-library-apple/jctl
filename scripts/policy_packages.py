#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Policy Packages

This script allows you to replace a lot of packages in policies at once. You
must know a little bit of Python to use this script. This script will not add
packages to policies. Use the GUI for that.

This script isn't standard by any measure. Running this script will generate a
list of policies and their packages. The script will attempt to do a prefix
match based on the regex '^...[^\\d]*' (the 1st three characters and every
character after that isn't a digit'). If it finds any unused packages that
match the prefix pattern, it will display it but have it commented out. Here's
an example of what it would print.

mass_edit = {
    'Install Zoom': [
        'Zoom-5.1.27838.0614.pkg',
#        'Zoom-5.1.28575.0629.pkg',
#        'Zoom-5.1.28648.0705.pkg',
    ],
}

Sooo... basically if you want replace the old Zoom package with a new one,
comment out the old one and uncomment the new one, and then, and here's where
it gets non-standard, *copy* the code and *paste* it into this script. That's
right, edit this script. Then run this script again. Magic.

To get it to display all of your policies and packages again, just make sure
you have the following variable empty.

mass_edit = {}

Remember, this script will not add packages to policies, only replace them.
And it will replace packages in the same order they are listed in the policy.
So if you've done any customization like specify an action or to update
autorun, those customizations will stick with the package that is in that
order.

For example, if you have a policy with 2 packages and the first package has
update autorun data checked, and you replace both packages with new ones, the
first one will still have update autorun data checked.

This script does not check the values for "Fill user templates (FUT)" or
"Fill existing user home directories (FEU)", which are package settings, not
policy settings. This matters because these settings are also stored in the
policy. So whatever the old package was, that's what the new package will be
too.
"""

__author__ = 'James Reynolds'
__email__ = 'reynolds@biology.utah.edu'
__copyright__ = 'Copyright (c) 2020, The University of Utah'
__license__ = 'MIT'
__version__ = "0.1"


import jamf
import re
from pprint import pprint

mass_edit = {
}

jss = jamf.API()
policies = jss.getNamedIds('policies')
pkgs = jss.getNamedIds('packages')
computer_grps = jss.getNamedDicts('computergroups')

if len(mass_edit) == 0:
    used_pkgs = {}
    for policy_name in policies:
        policy_id = policies[policy_name]
        policy = jss.get(f"policies/id/{policy_id}")

        policy_pkgs = jss.convertJSSPathToNamedIds(policy,['policy', 'package_configuration', 'packages', 'package'])
        if len(policy_pkgs) > 0:
            mass_edit[policy_name] = {'pkgs': policy_pkgs}
            for pkg_name in policy_pkgs:
                used_pkgs[pkg_name] = True

       policy_grps = jss.convertJSSPathToNamedIds(
           policy, ['policy', 'scope', 'computer_groups', 'computer_group'])
           
       if len(policy_grps) > 0:

           for policy_grp in policy_grps:

               if policy_grp in computer_grps:
                   if 'is_smart' in grps[policy_grp]:

                        print("------------------------------------")
                        print(f"{policy_name}")
#                         pprint(policy_grps)

#             new_list = []
#             for i in old_list:
#                 if filter(i):
#                     new_list.append(expressions(i))
#
#             new_list = [expression(i) for i in old_list if filter(i)]
#
#             filter: policy_grp in computer_grps and 'is_smart' in grps[policy_grp]

    unused_pkgs = list(filter(lambda i: i not in used_pkgs, pkgs))
    print("mass_edit = {")
    for policy_name in mass_edit:
        if len(mass_edit[policy_name]['pkgs']) > 1:
            print(f"    '{policy_name}': {{")
            print("        'pkgs': {")
            for pkg in mass_edit[policy_name]['pkgs']:
                print(f"            '{pkg}',")
                prefix = re.sub(r"^(...[^\d]*).*", "\\1", pkg)
                for unused_pkg in unused_pkgs:
                    if re.match(prefix, unused_pkg):
                        print(f"#            '{unused_pkg}',")
                        used_pkgs[unused_pkg] = True
        #print("        },")
        #print("        'grps': {")

# groups here

        print("        },")
        print("    },")
    print("}")
    print("# Unused Packages:")
    unused_pkgs = list(filter(lambda ii: ii not in used_pkgs, pkgs))
    for unused_pkg in unused_pkgs:
        print(f"#        '{unused_pkg}',")
else:
    for policy_name in mass_edit:
        print(f"Working on {policy_name}")
        pkg_arr = mass_edit[policy_name]['pkgs']
        if policy_name not in policies:
            print(f"ERROR: Policy \"{policy_name}\" is unknown")
            exit(1)
        policy_id = policies[policy_name]
        policy = jss.get(f"policies/id/{policy_id}")
        policy_pkgs = policy['policy']['package_configuration']['packages']
        for pkg_index, pkg_name in enumerate(pkg_arr):
            if pkg_name not in pkgs:
                print(f"ERROR: Package \"{pkg_name}\" is unknown")
                exit(1)
            if int(policy_pkgs['size']) != len(pkg_arr):
                print(f"ERROR: Policy \"{policy_name}\" has "
                      f"{policy_pkgs['size']} package(s) and "
                      f"you're trying to replace {len(pkg_arr)} package(s). "
                      f"You must specify the same number of packages.\n")
                exit(1)

            if policy_pkgs['size'] == '1':
                new_pkg_id = pkgs[pkg_name]
                policy_pkgs['package']['id'] = new_pkg_id
                policy_pkgs['package']['name'] = pkg_name
            else:
                new_pkg_id = pkgs[pkg_name]
                policy_pkgs['package'][pkg_index]['id'] = new_pkg_id
                policy_pkgs['package'][pkg_index]['name'] = pkg_name
        jss.put(f"policies/id/{policy_id}", policy)

# groups here

        grp_arr = mass_edit[policy_name]['grps']
