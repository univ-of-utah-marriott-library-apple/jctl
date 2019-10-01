# -*- coding: utf-8 -*-

"""
XML and JSON data conversion functions
"""

import os
import logging

from xml.etree import cElementTree as ElementTree
from collections import defaultdict


class Error(Exception):
    pass


def etree_to_dict_orig(t):
    """
    original function: https://stackoverflow.com/a/10077069/12020818
    contains additional
    """
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def etree_to_dict(x):
    """
    converts xml.cElementTree to python dict
    adapted from: https://stackoverflow.com/a/10077069/12020818
    removed attribute support
    """
    result = {x.tag: {}}
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
    converts python dict to xml string
    """
    if isinstance(data, dict):
        xml_str = ''
        for key, value in data.items():
            if isinstance(value, list):
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
        xml_str = f"{data}"
    
    return xml_str
        

def xml_to_dict(xml_string):
    logger = logging.getLogger(__name__)
    # logger.debug(f"converting xml: {xml_string!r}")
    root = ElementTree.XML(xml_string)
    return etree_to_dict(root)


if __name__ == '__main__':
    # fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    # logging.basicConfig(level=logging.DEBUG, format=fmt)
    pass
