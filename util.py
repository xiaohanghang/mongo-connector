"""A set of utilities used throughout the mongo-connector
"""

import sys
import time

from bson.timestamp import Timestamp
from pymongo import Connection
from urllib2 import urlopen


def verify_url(url):
    """Verifies the validity of a given url.
    """
    try:
        urlopen(url)
        return True
    except:
        return False


def bson_ts_to_long(timestamp):
    """Convert BSON timestamp into integer.

    Conversion rule is based from the specs
    (http://bsonspec.org/#/specification).
    """
    return ((timestamp.time << 32) + timestamp.inc)


def long_to_bson_ts(val):
    """Convert integer into BSON timestamp.
    """
    seconds = val >> 32
    increment = val & 0xffffffff

    return Timestamp(seconds, increment)


def retry_until_ok(func, args=None, no_func=False):
    """Retry code block until it succeeds.
    """

    result = True
    count = 0
    while True:
        try:
            if no_func is True:         # just a statement, not a function
                result = func
                break
            elif args is None:
                result = func()
                break
            else:
                result = func(args)
                break
        except:
            count += 1
            if count > 60:
                sys.exit(1)
            time.sleep(1)

    return result
