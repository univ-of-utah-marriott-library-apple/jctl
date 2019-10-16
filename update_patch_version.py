#!/usr/local/bin/python3

import sys
import logging
import plistlib
import argparse

import jamf

## GLOBALS

class Parser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        # self.parser.add_argument('-v', '--verbose', action='store_true', 
        #                          help='be verbose')
        # self.parser.add_argument('-d', '--debug', action='store_true',
        #                          help='be VERY verbose')
        # self.parser.add_argument('-V', '--version', action='store_true', 
        #                          help='print version and exit')

        self.parser.add_argument('-c', '--config', required=True,
                                 help='path to config')
        self.parser.add_argument('-t', '--tech', action='store')
        self.parser.add_argument('-g', '--guinea-pig', action='store')
        self.parser.add_argument('-s', '--stable', action='store')
        self.parser.add_argument('-p', '--pkg', nargs=2, default=[], action='append')
        # self.parser.add_argument('-l', '--list', action='store_true')
        self.parser.add_argument('name')
        
    def parse(self, argv):
        """
        :param argv:    list of arguments to parse
        :returns:       argparse.NameSpace object
        """
        return self.parser.parse_args(argv)



def config(plist):
    """
    loads configuration from plist
    :returns: address, (username, passwd)
    """
    with open(plist, 'rb') as f:
        c = plistlib.load(f)
    user, passwd = c['login'].split(':')
    return c['address'], (user, passwd)


def main(argv):
    logger = logging.getLogger(__name__)
    parser = Parser()
    args = parser.parse(argv)

    # address, auth = config('private/jss.plist')
    logger.debug(f"args: {args!r}")
    name = args.name
    v = {'Tech': args.tech, 
         'Guinea Pig': args.guinea_pig, 
         'Stable': args.stable}
    versions = {k:v for k, v in v.items() if v}
    pkgs = {x[0]: x[1] for x in args.pkg}

    logger.debug(f"NAME: {name}")
    logger.debug(f"VERSIONS: {versions!r}")
    logger.debug(f"PKGS: {pkgs!r}")

    address, auth = config(args.config)
    api = jamf.API(address, auth)
    
    jamf.patch.update_softwaretitle_versions(api, name, versions, pkgs)


if __name__ == '__main__':
    fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    main(sys.argv[1:])