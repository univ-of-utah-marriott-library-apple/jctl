#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import os

__all__ = (
	'string'
)

def string():
	try:
		with open(os.path.dirname(__file__) + "/VERSION", "r", encoding="utf-8") as fh:
			version = fh.read().strip()
			if version:
				return version
	except:
		pass
	return "0.0.0"
