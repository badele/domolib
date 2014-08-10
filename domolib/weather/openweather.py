#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#

import urllib, urllib2
import json


class openweather:

    def getweatherinfo(self, latitude, longitude):
        url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat=%s&lon=%s&units=metric&cnt=2" % (
            urllib.quote(str(latitude)), urllib.quote(str(longitude))
        )
        data = urllib.urlopen(url).read()
        dataopenweathermap = json.loads(data)

        return dataopenweathermap['list']

    def today(self, latitude, longitude):
        return self.getweatherinfo(latitude, longitude)[0]

    def tomorrowp(self, latitude, longitude):
        return self.getweatherinfo(latitude, longitude)[1]
