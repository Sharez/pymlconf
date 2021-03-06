# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore
"""
Created on:    Nov 17, 2013
@author:        vahid
"""
import sys

# noinspection PyBroadException
try:
    # Python 2.7+
    from collections import OrderedDict
except:
    # Python 2.6-
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    from ordereddict import OrderedDict


# For compatibility with python3
# TODO: When support for python 2.x is dropped,
# get rid of the import as well as substitute all basestring with str
try:
    # noinspection PyUnboundLocalVariable
    basestring = basestring
except NameError:
    basestring = str


def isiterable(o):
    if isinstance(o,(basestring, type)):
        return False
    elif hasattr(o, '__iter__'):
        return True
    else:
        return False 
    
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


# unittest compatibility
from unittest import TestCase
if sys.version_info >= (3, 0):  # Python 3.X
    TestCase.assertRegexpMatches = TestCase.assertRegex
    TestCase.assertNotRegexpMatches = TestCase.assertNotRegex
    
def read_file(file_path, encoding):
    if sys.version_info.major == 3:
        stream = open(file_path, encoding=encoding)
        return stream.read()
    else:
        stream = open(file_path)
        return stream.read().decode(encoding)
    stream.close()

        
