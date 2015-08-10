#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2015 Bruno Adelé'
__description__ = """Home automation library with command line interpreter"""
__license__ = 'GPL'
__version__ = '0.0.1'

# System
import sys
import pprint
import argparse

import domolib

def parse_arguments(cmdline=""):
    """Parse the arguments"""

    parser = argparse.ArgumentParser(
        description=__description__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-c', '--command',
        action='store',
        dest='command',
       help='Execute Commande'
    )

    parser.add_argument(
        '-s', '--select-field',
        action='store',
        dest='select',
       help='select only the field'
    )


    parser.add_argument(
        '-f', '--format',
        action='store',
        dest='format',
        default='flat',
        choices=[
            'flat',
            'json',
            'jsonflat',
        ],
        help='Format'
    )


    parser.add_argument(
        '-l', '--list',
        action='store_true',
        dest='list',
       help='List functions'
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

def listFunctions():
    infos = domolib.commons.plugins.get_plugins_informations()
    for modulename in infos.keys():
        # Calc funcdesk maxsize
        maxsize = 0
        for funcinfo in infos[modulename]:
            funcmethod = "%s(" % funcinfo['func']
            for param in funcinfo['params']:
                funcmethod += "%s, " % param

            funcmethod = "%s)" % funcmethod[:-2]


            maxsize = max(maxsize, len(funcmethod))

        # Show the plugin functions
        print " + %s" % modulename
        for funcinfo in infos[modulename]:
            funcmethod = "%s(" % funcinfo['func']
            for param in funcinfo['params']:
                funcmethod += "%s, " % param

            funcmethod = "%s)" % funcmethod[:-2]
            funcmethod = funcmethod.ljust(maxsize)
            funccomment = funcinfo['comment']
            print " | %(funcmethod)s  %(funccomment)s" % locals()
        print ""

def main():
    # Parse arguments
    args = parse_arguments(sys.argv[1:])  # pragma: no cover

    # Execute command and export
    if args.command:
        result = {}
        cmd = 'result = %s' % args.command
        exec(cmd)

        if args.select:
            result = eval(args.select)
            print result
            return

        if args.format == 'json':
            pprint.pprint(result, indent=2)

        if args.format == 'jsonflat':
            print flattenDict(result)

        if args.format == 'flat':
            print toTxt(flattenDict(result))


    if args.list:
        listFunctions()


if __name__ == '__main__':
    main()  # pragma: no cover

