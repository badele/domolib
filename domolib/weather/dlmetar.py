#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """A metar domolib"""
__license__ = 'GPL'
__version__ = '0.0.1'

# Require metar
# pip install metar

import re
import requests

from metar import Metar


class dlmetar():

    def __init__(self, **params):

            # Set parameters
            self.params = params
            self.results = {}

    def compute(self):
        # Get Metar information
        r = None
        r = requests.get("http://weather.noaa.gov/pub/data/observations/metar/stations/%s.TXT" % self.params['station'])
        print "http://weather.noaa.gov/pub/data/observations/metar/stations/%s.TXT" % self.params['station']

        if r is None or r.status_code != 200:
            return None

        # Extract only Metar informations
        m = re.search(
            '%s .*' % self.params['station'],
            r.content
        )

        if not m:
            return

        # Decode metar informations
        code = m.group(0)
        decode = Metar.Metar(code)

        # Get temperature
        if decode.temp:
            self.results['temp'] = decode.temp.value()

        # Get dewpt temperature
        if decode.dewpt:
            self.results['dewpt'] = decode.dewpt.value()

        # Get pressure
        if decode.press:
            self.results['pressure'] = decode.press.value()

        # Visibility
        print decode.vis
        if decode.vis:
            self.results['visibility'] = int(decode.vis.value())

        # Get wind speed
        if decode.wind_speed:
            self.results['wind_speed'] = decode.wind_speed.value() * 1.852

        # Calculate the relative humidity
        if decode.temp and decode.dewpt:
            temp = decode.temp.value()
            dewpt = decode.dewpt.value()
            self.results['humidity'] = round(100 * ((112 - 0.1 * temp + dewpt) / (112 + 0.9 * temp))**8, 2)

        # Calculate the wind chill or heat index
        if decode.temp and decode.wind_speed:
            speed = decode.wind_speed.value() * 1.852
            temp = decode.temp.value()
            self.results['wind_chill'] = round(13.12 + 0.6215*temp + (0.3965*temp - 11.37) * speed ** 0.16, 2)