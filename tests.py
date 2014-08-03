#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """Unittest"""
__license__ = 'GPLv3'


import unittest

from domolib.weather.dlmetar import dlmetar


class TestPackages(unittest.TestCase):

    def test_metar(self):

        # Init object
        metarobj = dlmetar(station='LFMT')
        metarobj.compute()

        # Check object
        self.assertTrue('wind_speed' in metarobj.results)
        self.assertTrue('temp' in metarobj.results)
        self.assertTrue('wind_chill' in metarobj.results)
        self.assertTrue('dewpt' in metarobj.results)
        self.assertTrue('visibility' in metarobj.results)
        self.assertTrue('humidity' in metarobj.results)
        self.assertTrue('pressure' in metarobj.results)

if __name__ == "__main__":
    unittest.main(verbosity=2)
