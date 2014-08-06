#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """Unittest"""
__license__ = 'GPLv3'


import unittest

from domolib.weather.dlmetar import dlmetar
from domolib.weather.vigimeteo import vigimeteo


class TestPackages(unittest.TestCase):

    def test_metar(self):

        # Init object
        obj = dlmetar()
        results = obj.getbulletin(station='LFMT')

        # Check object
        self.assertTrue('wind_speed' in results)
        self.assertTrue('temp' in results)
        self.assertTrue('wind_chill' in results)
        self.assertTrue('dewpt' in results)
        self.assertTrue('visibility' in results)
        self.assertTrue('humidity' in results)
        self.assertTrue('pressure' in results)

    def test_vigilance(self):
        obj = vigimeteo()
        results = obj.getvigilance('34')
        self.assertTrue('weatherlevelrisk' in results)
        self.assertTrue('risk' in results)
        self.assertTrue('floodlevelrisk' in results)

        # Check department 00 number
        results = obj.getvigilance('00')
        self.assertTrue(results is None)

        # Check department number error
        with self.assertRaises(Exception):
            obj.getvigilance('999')


if __name__ == "__main__":
    unittest.main(verbosity=2)
