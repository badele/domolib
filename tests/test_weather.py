#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """Unittest"""
__license__ = 'GPLv3'

import pytest

from domolib.weather.dlmetar import dlmetar
from domolib.weather.sunshine import sunshine
from domolib.weather.vigimeteo import vigimeteo
from domolib.weather.openweather import openweather


def test_metar():
    # Init object
    obj = dlmetar()
    results = obj.getbulletin(station='LFMT')

    # Check object
    assert 'wind_speed' in results
    assert 'temp' in results
    assert 'wind_chill' in results
    assert 'dewpt' in results
    assert 'visibility' in results
    assert 'humidity' in results
    assert 'pressure' in results


def test_sunshine():
    obj = sunshine()

    # Check sunshine not latitude and longitude set
    with pytest.raises(Exception):
        obj.getresults(latitude="43:36:43")

    with pytest.raises(Exception):
        obj.getresults(longitude="3:53:38")

    # check elevation is set
    obj.getresults(
        latitude="43:36:43", longitude="3:53:38", elevation=0,
        horizon_std="-0.833", horizon_civ="-6", horizon_nav="-12", horizon_ast="-18"
    )

    # test with Montpellier location and on 2014-08-08 20:10:00
    results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 00:00:00")

    # vars
    assert results['selected_time_ts'] == 1407456000

    assert results['sun_alt'] == -30
    assert results['sun_az'] == 2

    # Sunrise
    assert results['sunrise_std_ts'] == 1407472445
    assert results['sunrise_civ_ts'] == 1407470806
    assert results['sunrise_nav_ts'] == 1407468470
    assert results['sunrise_ast_ts'] == 1407465813

    # Sunset
    assert results['sunset_std_ts'] == 1407524718
    assert results['sunset_civ_ts'] == 1407526351
    assert results['sunset_nav_ts'] == 1407528674
    assert results['sunset_ast_ts'] == 1407531309

    # Night limit
    results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 0:00:00")
    assert results['sunshine_idx'] == 0
    results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 02:43:00")
    assert results['sunshine_idx'] == 0
    results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 02:44:00")
    assert results['sunshine_idx'] == 1


    # Astro limit
    results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 03:27:00")
    assert results['sunshine_idx'] == 1
    results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 03:28:00")
    assert results['sunshine_idx'] == 2

    # Naval limit
    results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 04:06:00")
    assert results['sunshine_idx'] == 2


    # Civil limit
    results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 04:34:00")
    assert results['sunshine_idx'] == 3

    results = obj.getresults(latitude="43:36:43", longitude="3:53:38", datetime="2014-08-08 04:36:00")
    assert results['sunshine_idx'] == 255


def test_vigilance():
    obj = vigimeteo()
    results = obj.getvigilance('34')
    assert 'weatherlevelrisk' in results
    assert 'risk' in results
    assert 'floodlevelrisk' in results

    # Check department 00 number
    results = obj.getvigilance('00')
    assert results is None

    # Check department number error
    with pytest.raises(Exception):
        obj.getvigilance('999')


def test_openweather():
    obj = openweather()
    results = obj.today(latitude=43.61, longitude=3.88)
    assert 'clouds' in results
    assert 'deg' in results
    assert 'humidity' in results
    assert 'pressure' in results
    assert 'speed' in results
    assert 'temp' in results
    assert 'weather' in results

    results = obj.tomorrowp(latitude=43.61, longitude=3.88)
    assert 'clouds' in results
    assert 'deg' in results
    assert 'humidity' in results
    assert 'pressure' in results
    assert 'speed' in results
    assert 'temp' in results
    assert 'weather' in results