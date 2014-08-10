#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """Unittest"""
__license__ = 'GPLv3'


import unittest

from domolib.weather.dlmetar import dlmetar
from domolib.weather.sunshine import sunshine
from domolib.weather.vigimeteo import vigimeteo
from domolib.weather.openweather import openweather


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

    def test_sunshine(self):
        obj = sunshine()

        # Check sunshine not latitude and longitude set
        with self.assertRaises(Exception):
            obj.getresults(latitude="43:36:43")

        with self.assertRaises(Exception):
            obj.getresults(longitude="3:53:38")

        # check elevation is set
        obj.getresults(
            latitude="43:36:43", longitude="3:53:38", elevation=0,
            horizon_std="-0.833", horizon_civ="-6", horizon_nav="-12", horizon_ast="-18"
        )

        # test with Montpellier location and on 2014-08-08 20:10:00
        results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 00:00:00")

        # vars
        self.assertTrue(results['selected_time_ts'] == 1407456000)

        self.assertTrue(results['sun_alt'] == -30)
        self.assertTrue(results['sun_az'] == 2)

        # Sunrise
        self.assertTrue(results['sunrise_std_ts'] == 1407472445)
        self.assertTrue(results['sunrise_civ_ts'] == 1407470806)
        self.assertTrue(results['sunrise_nav_ts'] == 1407468470)
        self.assertTrue(results['sunrise_ast_ts'] == 1407465813)

        # Sunset
        self.assertTrue(results['sunset_std_ts'] == 1407524718)
        self.assertTrue(results['sunset_civ_ts'] == 1407526351)
        self.assertTrue(results['sunset_nav_ts'] == 1407528674)
        self.assertTrue(results['sunset_ast_ts'] == 1407531309)

        # Night limit
        results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 0:00:00")
        self.assertTrue(results['sunshine_idx'] == 0)
        results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 02:43:00")
        self.assertTrue(results['sunshine_idx'] == 0)
        results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 02:44:00")
        self.assertTrue(results['sunshine_idx'] == 1)


        # Astro limit
        results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 03:27:00")
        self.assertTrue(results['sunshine_idx'] == 1)
        results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 03:28:00")
        self.assertTrue(results['sunshine_idx'] == 2)

        # Naval limit
        results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 04:06:00")
        self.assertTrue(results['sunshine_idx'] == 2)


        # Civil limit
        results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 04:34:00")
        self.assertTrue(results['sunshine_idx'] == 3)

        results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 04:36:00")
        self.assertTrue(results['sunshine_idx'] == 255)

    def test_openweather(self):
        obj = openweather()
        results = obj.today(latitude=43.61, longitude=3.88)
        self.assertTrue('clouds' in results)
        self.assertTrue('deg' in results)
        self.assertTrue('humidity' in results)
        self.assertTrue('pressure' in results)
        self.assertTrue('speed' in results)
        self.assertTrue('temp' in results)
        self.assertTrue('weather' in results)

        results = obj.tomorrowp(latitude=43.61, longitude=3.88)
        self.assertTrue('clouds' in results)
        self.assertTrue('deg' in results)
        self.assertTrue('humidity' in results)
        self.assertTrue('pressure' in results)
        self.assertTrue('speed' in results)
        self.assertTrue('temp' in results)
        self.assertTrue('weather' in results)


if __name__ == "__main__":
    unittest.main(verbosity=2)
