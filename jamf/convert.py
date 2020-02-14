# -*- coding: utf-8 -*-

"""
XML and JSON data conversion functions
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.2.2"

from xml.etree import cElementTree as ElementTree
import xml.sax.saxutils
from collections import defaultdict


class Error(Exception):
    pass


def etree_to_dict(x):
    """
    converts xml.cElementTree to python dict
    adapted from: https://stackoverflow.com/a/10077069/12020818
    removed attribute support
    """
    result = {x.tag: None}
    children = list(x)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        result = {x.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    elif x.text:
        result[x.tag] = x.text.strip()

    return result


def dict_to_xml(data):
    """
    Convert python dict to xml string
    :returns:  xml string
    """
    if isinstance(data, dict):
        xml_str = ''
        for key, value in data.items():
            if value is None:
                xml_str += f"<{key}/>"
            elif isinstance(value, list):
                # if the value is a list, wrap each entry with the key
                for i in value:
                    result = dict_to_xml(i)
                    xml_str += f"<{key}>{result}</{key}>"
            else:
                # otherwise, wrap the entire result
                result = dict_to_xml(value)
                xml_str += f"<{key}>{result}</{key}>"
    elif isinstance(data, list):
        raise Error("unable to properly tag nested lists")
    else:
        # string, boolean, integers, floats, etc
        xml_str = xml.sax.saxutils.escape(f"{data}")

    return xml_str


def xml_to_dict(xml_string):
    """
    Convert xml string to python dict
    :returns:  dict
    """
    root = ElementTree.XML(xml_string)
    return etree_to_dict(root)
