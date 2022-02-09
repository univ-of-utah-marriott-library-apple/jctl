#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
update asset tag field for ALL Jamf computers from CSV
"""

__author__ = "Sam Forester"
__license__ = "MIT"

import csv
import logging
import jamf

# create inventory lookup for each asset tag by serial number
with open("asset_inventory.csv", "r") as f:
    inventory = {r["SERIAL_NUMBER"]: r["ASSET_TAG"] for r in csv.DictReader(f)}

# iterate all Jamf computer records
for computer in jamf.Computers():
    # get serial number from Jamf computer record
    serial_number = computer.data["general"]["serial_number"]
    try:
        # lookup asset tag from inventory using serial number
        asset_tag = inventory[serial_number]
    except KeyError:
        # serial number not recorded in csv file (skip Jamf computer record)
        logging.error(f"{computer}: {serial_number}: no asset information")
        continue
    # check Jamf computer record asset tag, update if blank/incorrect
    if asset_tag != computer.data["general"]["asset_tag"]:
        computer.data["general"]["asset_tag"] = asset_tag
        computer.save()
