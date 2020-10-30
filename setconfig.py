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


import sys
import logging
import pprint
import pathlib
import argparse

import jamf
import jamf.admin
from jamf.package import Package
import jamf.config


class Parser:

    def __init__(self):
        self.parser = argparse.ArgumentParser()

        desc = 'see `%(prog)s COMMAND --help` for more information'
        self.subparsers = self.parser.add_subparsers(title='COMMANDS',
                                                     dest='cmd',
                                                     description=desc)
        # listing
        test = self.subparsers.add_parser('test', help='Test',
                                          description="tests the config")

        # config
        config = self.subparsers.add_parser('config', help='modify config',
                                            description="modify config")
        config.add_argument('-H', '--hostname',
                            help='use username instead of prompting')
        config.add_argument('-u', '--user',
                            help='use username instead of prompting')
        config.add_argument('-p', '--passwd',
                            help='specify password (default: prompt)')
        config.add_argument('-c', '--config', dest='path', metavar='PATH',
                            help=f"specify config file (default: {jamf.config.PREFERENCES})")
        config.add_argument('-d', '--delete', action='store_true',
                            help='delete existing config profile')

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

    api = jamf.API()

    if args.cmd == 'test':
        logger.debug("creating api")
        jss = jamf.API()
        pprint.pprint(jss.get('accounts'))

    elif args.cmd == 'config':
        conf = jamf.config.SecureConfig(args.path)
        if args.delete:
            conf.reset()
            raise SystemExit(f"deleted: {conf.path}")
        hostname = args.hostname
        if hostname:
            conf.set('JSSHostname', hostname)
        else:
            hostname = conf.get('JSSHostname', prompt='JSS Hostname')
        a = (args.user, args.passwd)
        auth = a if all(a) else jamf.config.credentials_prompt(args.user)
        conf.credentials(hostname, auth)
        conf.save()


if __name__ == '__main__':
    fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    main(sys.argv[1:])
