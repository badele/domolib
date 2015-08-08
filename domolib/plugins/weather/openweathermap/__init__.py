#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#

try:
    from urllib.request import urlopen, quote
except ImportError:
    from urllib import urlopen, quote

import json


class openweather:

    def getweatherinfo(self, latitude, longitude):
        url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat=%s&lon=%s&units=metric&cnt=2" % (
            quote(str(latitude)), quote(str(longitude))
        )
        data = urlopen(url).read().decode('utf-8')
        dataopenweathermap = json.loads(data)

        return dataopenweathermap['list']

    def today(self, latitude, longitude):
        return self.getweatherinfo(latitude, longitude)[0]

    def tomorrowp(self, latitude, longitude):
        return self.getweatherinfo(latitude, longitude)[1]
