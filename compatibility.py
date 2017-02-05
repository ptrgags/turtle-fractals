"""
Compatibility module since I don't need something as big as six.py
"""
import sys

if sys.version_info < (3,):
    range = xrange
else:
    range = range
