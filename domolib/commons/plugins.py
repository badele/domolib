import os
import re
import sys
import fnmatch
import inspect
import importlib
import textwrap

import domolib

def get_plugins_informations():
    plugins_patch =  os.path.dirname(domolib.plugins.__file__)

    # Search modules
    modules = []
    for root, dirnames, filenames in os.walk(plugins_patch):
        for filename in fnmatch.filter(filenames, '__init__.py'):
            fullname = '%(root)s/%(filename)s' % locals()

            rpattern = '%(plugins_patch)s/(.*?)/(.*?)/.*?\.py' % locals()
            importedmod = re.match(rpattern, fullname)
            if importedmod:
                modinfo = {
                    'category': importedmod.group(1),
                    'modulename': importedmod.group(2),
                }
                modules.append(modinfo)

    # Search dedcorated plugin command
    decorated = {}
    for modinfo in modules:
        mcategory = modinfo['category']
        mname = modinfo['modulename']

        # Load plugin module
        modname = 'domolib.plugins.%(mcategory)s.%(mname)s' % locals()
        importedmod = importlib.import_module(modname)
        members = inspect.getmembers(importedmod)

        # Search decorated function
        for objname, obj in members:
            isdecorated = hasattr(obj, 'domolib_decorated')
            if isdecorated:
                params = []
                if obj.__doc__:
                    lines = obj.__doc__.strip().splitlines()

                    comment = lines[0]
                    for line in lines:
                        m = re.match('.*:param (.*):.*', line)
                        if m:
                            params.append(m.group(1))

                funcinfo = {
                    'func': objname,
                    'comment': comment,
                    'params': params
                }

                if modname in decorated:
                    decorated[modname].append(funcinfo)
                else:
                    decorated[modname] = [funcinfo]

        del importedmod

    return decorated

