#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Update Jamf Patch Policies

Examples:

# Assign "firefox_70.0.1_2019.10.31_rcg.pkg" to patch version "70.0.1"
$> update_patch.py --pkg 70.0.1 firefox_70.0.1_2019.10.31_rcg.pkg "Mozilla Firefox"

# Set Firefox version to "70.0.1" for Tech Branch
$> update_patch.py --tech 70.0.1 "Mozilla Firefox"

# Set Firefox version to "70.0" for Stabe Branch
$> update_patch.py --stable 70.0 "Mozilla Firefox"

# Compounding:
# For Firefox:
#   Assign Packages:
#       72.0   -> firefox_72.0_2020.01.08_rcg.pkg
#       72.0.1 -> firefox_72.0.1_2020.01.09_rcg.pkg
#       72.0.2 -> firefox_72.0.2_2020.01.23_rcg.pkg
#   Branching:
#              Tech -> 72.0.2
#       Guinea-Pigs -> 72.0.1
#            Stable -> 72.0

$> update_patch.py -p 72.0 firefox_72.0_2020.01.08_rcg.pkg \
-p 72.0.1 firefox_72.0.1_2020.01.09_rcg.pkg \
-p 72.0.2 firefox_72.0.2_2020.01.23_rcg.pkg \
-t 72.0.2 -g 72.0.1 -s 72.0  "Mozilla Firefox"

"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2020 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "1.0.4"
min_jamf_version = "0.6.9"


import sys
import logging
import pprint
import pathlib
import argparse

import jamf
#import jamf.admin
from jamf.package import Package
#import jamf.config


class Parser:

    def __init__(self):
        self.parser = argparse.ArgumentParser()

        desc = 'see `%(prog)s COMMAND --help` for more information'
        self.subparsers = self.parser.add_subparsers(title='COMMANDS',
                                                     dest='cmd',
                                                     description=desc)
        # listing
        list = self.subparsers.add_parser('list', help='without arguments, lists all names of all SoftwareTitles',
                                          description="list patch info")
        list.add_argument('-v', '--versions', action='store_true',
                          help='list SoftwareTitle versions and packages for NAME')
        list.add_argument('-P', '--patches', action='store_true',
                          help='list patch policies current versions for SoftwareTitle NAME')
        list.add_argument('-p', '--pkgs', action='store_true',
                          help='list jss packages starting with NAME (or all if no NAME)')
        list.add_argument('name', metavar='NAME', action='store', nargs='?',
                          help='contextual name specification')
        list.add_argument('-i', '--ids', action='store_true',
                          help='list all Policies with IDs')

        # updating
        update = self.subparsers.add_parser('update', help='update patch',
                                            description="update patch software titles and policies")
        update.add_argument('-p', '--pkg', nargs=2,
                            metavar=("ver", "pkg"),
                            default=[], action='append',
                            help='update package for SoftwareTitle version')
        update.add_argument('-t', '--tech', action='store',
                            metavar='ver',
                            help='specify version of Tech')
        update.add_argument('-g', '--guinea-pig', action='store',
                            metavar='ver',
                            help='specify version of Guinea Pigs')
        update.add_argument('-s', '--stable', action='store',
                            metavar='ver',
                            help='specify version of Stable')
        update.add_argument('name', metavar='NAME', help='name of SoftwareTitles')

        # information
        info = self.subparsers.add_parser('info', help='get info about packages',
                                          description="get info need for patch definitions")
        info.add_argument('path', metavar='PACKAGE', help='path to package')

        # upload packages
        upload = self.subparsers.add_parser('upload', help='upload packages',
                                            description="upload a package")
        upload.add_argument('path', metavar='PACKAGE', help='path to package')
        upload.add_argument('-f', '--force', action='store_true',
                            help='force package re-upload')

        # remove packages
        remove = self.subparsers.add_parser('remove', help='remove packages',
                                            description="remove a package")
        remove.add_argument('name', metavar='PACKAGE', help='name of package')
        # upload.add_argument('-f', '--force', help='force package re-upload')

    def parse(self, argv):
        """
        :param argv:    list of arguments to parse
        :returns:       argparse.NameSpace object
        """
        return self.parser.parse_args(argv)

def check_version():
    python_jamf_version = jamf.version.jamf_version_up_to(min_jamf_version)
    if python_jamf_version != min_jamf_version:
        print(f"patch.py requires python-jamf {min_jamf_version} or newer. "
              f"You have {python_jamf_version}.")
        exit()

def print_version_key_list(versions):
    """
    Prints formatted (justified) list of key/value tuple pairs

    e.g.  [('1.0', 'justified text'),
           ('1.0.0', '-'),
           ('2.0', ''),
           ('2.0.0.2.a', 'longest version key')]
    would print:
    '''
      1.0:        justified text
      1.0.0:      -
      2.0:
      2.0.0.2.a:  longest version key
    '''

    :param versions <list>:  list of tuple key/value pairs
                              e.g. [('1.O', 'info'), ('1.0.0', 'more'), ...]
    """
    # get length of the longest key
    longest = sorted([len(k) for k, v in versions])[-1]
    for ver, value in versions:
        # dynamic right-justification of value based on longest version key
        justification = (longest - len(ver)) + len(value)
        print(f"  {ver}:  {value:>{justification}}")


def list_softwaretitles(api, name=None):
    p = api.get('patchsoftwaretitles')
    titles = p['patch_software_titles']['patch_software_title']
    if name:
        # only names that start with name (case-sensitive)
        result = [x['name'] for x in titles if x['name'].startswith(name)]
    else:
        # all names
        result = [x['name'] for x in titles]
    # print sorted list of resulting Patch SoftwareTitle names
    for n in sorted(result):
        print(n)


def list_packages(api, name=None):
    p = api.get('packages')
    pkgs = p['packages']['package']
    if name:
        # only names that start with name (case-sensitive)
        result = [x['name'] for x in pkgs if x['name'].lower().startswith(name.lower())]
    else:
        # all names
        result = [x['name'] for x in pkgs]
    # print sorted list of resulting Patch SoftwareTitle names
    for n in sorted(result):
        print(n)


def list_policies_ids(api, name):
    p = api.get('policies')
    pls = p['policies']['policy']
    ids = [x['id'] for x in pls]
    id_name = [x['name'] for x in pls]
    return(ids, id_name)


def print_policies_ids(api, name):
    (ids, id_name) = list_policies_ids(api, name)
    for b in range(len(ids)):
        #print(b)
        print("ID: " + ids[b] + " Name: " + id_name[b])


def list_softwaretitle_versions(api, name):
    title = find_softwaretitle(api, name)['patch_software_title']
    versions = []
    # get each version and assoiciated package (if one)
    for version in title['versions']['version']:
        v = version['software_version']
        # {name of pkg} or '-'
        p = version['package']['name'] if version['package'] else '-'
        versions.append((v, p))
    # print formatted result
    print_version_key_list(versions)


def list_softwaretitle_policy_versions(api, name):
    jssid = find_softwaretitle(api, name, details=False)['id']
    versions = []
    for patch in softwaretitle_policies(api, jssid):
        p = api.get(f"patchpolicies/id/{patch['id']}")
        version = p['patch_policy']['general']['target_version']
        versions.append((version, patch['name']))
    # print formatted result
    print_version_key_list(versions)


def find_softwaretitle(api, name, details=True):
    """
    :param api:         jamf.api.API object
    :param name:        name of softwaretitle
    :param details:     if False, return simple (id + name) (default: True)

    :returns:           patch softwaretitle information
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"looking for existing software title: {name}")
    # Iterate all Patch Management Titles for specified matching name
    data = api.get('patchsoftwaretitles')['patch_software_titles']
    for title in data['patch_software_title']:
        if title['name'] == name:
            logger.debug(f"found title: {name!r}")
            if details:
                logger.debug("returning detailed title info")
                jssid = title['id']
                return api.get(f"patchsoftwaretitles/id/{jssid}")
            else:
                logger.debug("returning simple title info")
                return title
    raise ValueError(f"missing software title: {name!r}")


def softwaretitle_policies(api, jssid):
    """
    :returns: list of software title patch policies
    """
    endpoint = f"patchpolicies/softwaretitleconfig/id/{jssid}"
    return api.get(endpoint)['patch_policies']['patch_policy']


def update_softwaretitle_versions(api, name, versions, pkgs=None):
    """
    Update all
    :param api:      JSS API object
    :param name:     name of external patch definition
    :param versions: {'Tech': version, 'Guinea Pig': version, 'Stable': version}

    :returns:
    """
    logger = logging.getLogger(__name__)
    jssid = find_softwaretitle(api, name, details=False)['id']

    if pkgs:
        update_softwaretitle_packages(api, jssid, pkgs)

    for p in softwaretitle_policies(api, jssid):
        # 'Tech - Test Boxes - Keynote' -> 'Tech'
        # 'Guinea Pig - Lab - Xcode' -> 'Guinea Pig'
        branch = p['name'].split(' - ')[0]
        try:
            update_patch_policy_version(api, p['id'], versions[branch])
        except KeyError:
            logger.debug(f"skipping: {p['name']!r}")


def update_patch_policy_version(api, jssid, version):
    """
    Update Patch Policy version
    """
    logger = logging.getLogger(__name__)
    current = api.get(f"patchpolicies/id/{jssid}")
    current_version = current['patch_policy']['general']['target_version']
    name = current['patch_policy']['general']['name']

    if current_version != version:
        logger.info(f"updating: {name!r}: {version}")
        data = {'patch_policy': {'general': {'target_version': version}}}
        api.put(f"patchpolicies/id/{jssid}", data)
    else:
        logger.debug(f"already updated: {name}: {version}")


def update_softwaretitle_packages(api, jssid, pkgs):
    """
    Update packages of software title

    :param jssid:        Patch Software Title ID
    :param pkgs:         dict of {version: package, ...}

    :returns: None
    """
    logger = logging.getLogger(__name__)

    data = api.get(f"patchsoftwaretitles/id/{jssid}")
    title = data['patch_software_title']

    title_name = title['name']
    logger.info(f"updating patch software title: {title_name} ({jssid})")

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
        result = api.put(f"patchsoftwaretitles/id/{jssid}", data)
        logger.info(f"succesfully updated: {title_name}")
        return result
    else:
        logger.info(f"software title was not modified")


def package_notes(path):
    path = pathlib.Path(path)
    *name, ver, date, author = path.stem.split('_')
    return f"{date}, {author.upper()}"


def main(argv):
    logger = logging.getLogger(__name__)
    args = Parser().parse(argv)
    logger.debug(f"args: {args!r}")

    api = jamf.API()

    if args.cmd == 'list':
        if args.versions:
            # `patch.py list --versions NAME`
            if not args.name:
                raise SystemExit("ERROR: must specify SoftwareTitle name")
            list_softwaretitle_versions(api, args.name)
        elif args.patches:
            # `patch.py list --patches NAME`
            if not args.name:
                raise SystemExit("ERROR: must specify SoftwareTitle name")
            list_softwaretitle_policy_versions(api, args.name)
        elif args.pkgs:
            # `patch.py list --pkgs`
            list_packages(api, args.name)
        elif args.ids:
            # `patch.py list --ids`
            print_policies_ids(api, args.name)
        else:
            # `patch.py list`
            list_softwaretitles(api, args.name)

    elif args.cmd == 'update':
        # update patch software titles and/or patch policies
        v = {'Tech': args.tech,
             'Guinea Pig': args.guinea_pig,
             'Stable': args.stable}
        versions = {k:v for k, v in v.items() if v}
        pkgs = {x[0]: x[1] for x in args.pkg}

        logger.debug(f"NAME: {args.name}")
        logger.debug(f"VERSIONS: {versions!r}")
        logger.debug(f"PKGS: {pkgs!r}")

        update_softwaretitle_versions(api, args.name, versions, pkgs)

    elif args.cmd == 'info':
        pprint.pprint(Package(args.path).apps)

    elif args.cmd == 'upload':
        pkg = Package(args.path)
        # try:
        #     info = pkg.info
        # except Exception:
        #     raise SystemExit(f"invalid package: {args.path!r}")
        admin = jamf.admin.JamfAdmin()
        #admin = jamf.Admin()
        try:
            uploaded = admin.add(pkg)
        except jamf.admin.DuplicatePackageError as e:
            if not args.force:
                raise e
            uploaded = admin.find(pkg.name)
        admin.update(uploaded, notes=package_notes(uploaded.path))

    elif args.cmd == 'remove':
        path = pathlib.Path(args.name)
        if path.name != str(path):
            raise SystemExit("must specify package name not path")
        admin = jamf.JamfAdmin()
        try:
            pkg = admin.find(path.name)
        except jamf.admin.MissingPackageError:
            logger.error(f"package already removed: {path.name}")
        else:
            admin.delete(pkg)



if __name__ == '__main__':
    check_version()
    fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    main(sys.argv[1:])
