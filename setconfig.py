#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jamf Config
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2020 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "1.0.4"

import argparse
import getpass
import jamf
import logging
import platform
import pprint
import sys

class Parser:

    def __init__(self):
        myplatform = platform.system()
        if myplatform == "Darwin":
            default_pref = jamf.config.MACOS_PREFS
        elif myplatform == "Linux":
            default_pref = jamf.config.LINUX_PREFS

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '-H',
            '--hostname',
            help='specify hostname (default: prompt)')
        self.parser.add_argument(
            '-u',
            '--user',
            help='specify username (default: prompt)')
        self.parser.add_argument(
            '-p',
            '--passwd',
            help='specify password (default: prompt)')
        self.parser.add_argument(
            '-c',
            '--config',
            dest='path',
            metavar='PATH',
            default=default_pref,
            help=f"specify config file (default {default_pref})")
        self.parser.add_argument(
            '-P',
            '--print',
            action='store_true',
            help='print existing config profile (except password!)')
        self.parser.add_argument(
            '-t',
            '--test',
            action='store_true',
            help='Connect to the Jamf server using the config file')

    def parse(self, argv):
        """
        :param argv:    list of arguments to parse
        :returns:       argparse.NameSpace object
        """
        return self.parser.parse_args(argv)


def main(argv):
    logger = logging.getLogger(__name__)
    args = Parser().parse(argv)
    logger.debug(f"args: {args!r}")

    if args.test:
        api = jamf.API()
        pprint.pprint(api.get('accounts'))

    elif args.print:
        conf = jamf.config.Config(prompt=False)
        print(conf.hostname)
        print(conf.username)
        if conf.password:
            print("Password is set")
        else:
            print("Password is not set")
    else:
        if args.path:
            config_path = args.path
        else:
            config_path = self.default_pref

        if args.hostname:
            hostname = args.hostname
        else:
            hostname = jamf.config.prompt_hostname()

        if args.user:
            user = args.user
        else:
            user = input("username: ")

        if args.passwd:
            passwd = args.passwd
        else:
            passwd = getpass.getpass()

        conf = jamf.config.Config(
            config_path=config_path,
            hostname=hostname,
            username=user,
            password=passwd,
            prompt=False
        )
        conf.save()


if __name__ == '__main__':
    fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    main(sys.argv[1:])
