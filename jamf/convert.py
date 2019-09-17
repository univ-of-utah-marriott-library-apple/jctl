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


def etree_to_dict2(x):
    """
    converts xml.cElementTree to python dict
    
    adapted from: https://stackoverflow.com/a/10077069/12020818
    I removed the attribute functionality
    """
    d = {x.tag: {}}
    # only tagged elements are returned in list? (i.e. not text elements?)
    children = list(x)
    if children:
        # I've never fully understood defaultdict
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            # I think this is the exposed result of the recursive function
            for k, v in dc.items():
                dd[k].append(v)
        # obviously does most the heavy lifting (utilizes defaultdict?)
        d = {x.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    elif x.text:
        text = x.text.strip()

        if text.lower() == 'true':
            d[x.tag] = True
        elif text.lower() == 'false':
            d[x.tag] = False
        else:        
            try:
                d[x.tag] = int(text)
            except ValueError:
                d[x.tag] = text
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


def dict_to_xml(d):
    """
    converts python dict to xml string
    """
    if isinstance(d, dict):
        xml_str = ''
        for key, value in d.items():
            result = xml_from_dict(value)
            xml_str += f"<{key}>{result}</{key}>"
    elif isinstance(d, list):
        xml_str = xml_from_dict(value)
    else:
        xml_str = f"{d}"
    
    return xml_str


def dict_to_xml2(data):
    """
    converts python dict to xml string
    """
    if isinstance(data, dict):
        xml_str = ''
        for key, value in data.items():
            result = xml_from_dict(value)
            xml_str += f"<{key}>{result}</{key}>"
    elif isinstance(data, list):
        xml_str = xml_from_dict(value)
    else:
        xml_str = f"{data}"
    
    return xml_str
        

def xml_to_dict(xml_string):
    logger = logging.getLogger(__name__)
    logger.debug(f"converting xml: {xml_string!r}")
    root = ElementTree.XML(xml_string)
    return etree_to_dict(root)


if __name__ == '__main__':
    # fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    # logging.basicConfig(level=logging.DEBUG, format=fmt)
    pass
