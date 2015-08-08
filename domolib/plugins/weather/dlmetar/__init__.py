#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """A metar domolib"""
__license__ = 'GPL'
__version__ = '0.0.1'

# Require metar
# pip install git+https://github.com/tomp/python-metar.git

import re

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

from metar import Metar
from domolib.commons.decorator import command


class dlmetar():
    def getbulletin(self, station):
        results = {}

        # Get Metar information
        url = 'http://weather.noaa.gov/pub/data/observations/metar/stations'

        r = None
        r = urlopen('%s/%s.TXT' % (url, station))

        if r.getcode() is None or r.getcode() != 200:
            return None

        # Extract only Metar informations
        m = re.search(
            '%s .*' % station,
            r.read().decode('utf-8')
        )

        if not m:
            return

        # Decode metar informations
        code = m.group(0)
        decode = Metar.Metar(code)

        # Get temperature
        if decode.temp:
            results['temp'] = decode.temp.value()

        # Get dewpt temperature
        if decode.dewpt:
            results['dewpt'] = decode.dewpt.value()

        # Get pressure
        if decode.press:
            results['pressure'] = decode.press.value()

        # Visibility
        if decode.vis:
            results['visibility'] = int(decode.vis.value())

        # Get wind speed
        if decode.wind_speed:
            results['wind_speed'] = decode.wind_speed.value() * 1.852

        # Calculate the relative humidity
        if decode.temp and decode.dewpt:
            temp = decode.temp.value()
            dewpt = decode.dewpt.value()
            results['humidity'] = round(
                100 * ((112 - 0.1 * temp + dewpt) / (112 + 0.9 * temp)) ** 8,
                2
            )

        # Calculate the wind chill or heat index
        if decode.temp and decode.wind_speed:
            speed = decode.wind_speed.value() * 1.852
            temp = decode.temp.value()
            results['wind_chill'] = round(
                13.12 + 0.6215 * temp +
                (0.3965 * temp - 11.37) * speed ** 0.16,
                2
            )

        return results

@command
def get_metarinfo(oaci,toto):
    """
    Get a weather from metar report
    :param oaci:
    :param toto:
    :return:
    """
    pass

@command
def get_metarlistinfo(oaci):
    """
    Get a OACI metar report from list airport
    :param oaci:
    :param toto:
    :return:
    """
    pass
