#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2015 Bruno Adelé'
__description__ = """timeseries database with reduce system"""
__license__ = 'GPL'
__version__ = '0.0.1'

# System
import sys
import argparse
import pprint

from domolib import *

def parse_arguments(cmdline=""):
    """Parse the arguments"""

    parser = argparse.ArgumentParser(
        description=__description__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-a', '--action',
        action='store',
        dest='action',
       help='Action'
    )

    parser.add_argument(
        '-f', '--format',
        action='store',
        dest='format',
        default='json',
        choices=[
            'flat',
            'json',
            'jsonflat',
        ],
        help='Format'
    )


    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__)
    )

    # Check if the command line contains arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    a = parser.parse_args(cmdline)
    return a


def flattenDict(d, result=None):
    """
    https://gist.github.com/higarmi/6708779
    :param d:
    :param result:
    :return:
    """
    if result is None:
        result = {}
    for key in d:
        value = d[key]
        if isinstance(value, dict):
            value1 = {}
            for keyIn in value:
                value1[".".join([key,keyIn])]=value[keyIn]
            flattenDict(value1, result)
        elif isinstance(value, (list, tuple)):
            for indexB, element in enumerate(value):
                if isinstance(element, dict):
                    value1 = {}
                    index = 0
                    for keyIn in element:
                        newkey = ".".join([key,keyIn])
                        value1[".".join([key,keyIn])]=value[indexB][keyIn]
                        index += 1
                    for keyA in value1:
                        flattenDict(value1, result)
        else:
            result[key]=value
    return result


def toTxt(dictvalue):
    result = ''
    keys = dictvalue.keys()

    # Get max len keyname
    maxlen = 0
    for key in keys:
        maxlen = max(maxlen, len(key))

    for key in sorted(keys):
        keyname = key.ljust(maxlen)
        value = dictvalue[key]
        result += '%(keyname)s: %(value)s\n' % locals()

    return result

def main():
    # Parse arguments
    args = parse_arguments(sys.argv[1:])  # pragma: no cover

    # Execute command and export
    if args.action:
        result = eval(args.action)

        if args.format == 'json':
            pprint.pprint(result, indent=2)

        if args.format == 'jsonflat':
            print flattenDict(result)

        if args.format == 'flat':
            print toTxt(flattenDict(result))

if __name__ == '__main__':
    #  domolib_cmd.py -a "weather.dlmetar.dlmetar().getbulletin(station='LFMT')" -f flat
    main()  # pragma: no cover
