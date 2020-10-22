#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Tony Williams'
__email__ = 'tonyw@honestpuck.com'
__copyright__ = 'Copyright (c) 2020 Tony Williams'
__license__ = 'MIT'
__date__ = '2020-10-08'
__version__ = "0.2.0"


import jamf

groups = jamf.ComputerGroups()

a_group = groups.get('Last Check-in >30 Days')

for computer in a_group['computers']['computer']:
    print(computer['id'])

computers = jamf.Computers()

for computer in a_group['computers']['computer']:
    this = computers.get(computer['id'])
    serial = this['general']['serial_number']
    name = this['location']['real_name']
    email = this['location']['email_address']
    print("%s, %s, %s" % (serial, name,email))
