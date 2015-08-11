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

from domolib.commons.decorator import command
from domolib.commons import cache


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

    def tomorrow(self, latitude, longitude):
        return self.getweatherinfo(latitude, longitude)[1]

@command
def get_today_weather(latitude, longitude):
    """
    Get today weather
    :param latitude:
    :param longitude:
    :return:
    """
    # Get result from cache
    mycache = cache.cache(cachefile='openweather.get_today_weather')
    result = mycache.getcachedresults()
    if result:
        return result

    # Compute the result and store in the cache file
    obj = openweather()
    result  = obj.today(latitude, longitude)
    mycache.setcacheresults(result)

    return result

@command
def get_tomorrow_weather(latitude, longitude):
    """
    Get tomorrow weather
    :param latitude:
    :param longitude:
    :return:
    """
    # Get result from cache
    mycache = cache.cache(cachefile='openweather.get_tomorrow_weather')
    result = mycache.getcachedresults()
    if result:
        return result

    # Compute the result and store in the cache file
    obj = openweather()
    result  = obj.tomorrow(latitude, longitude)
    mycache.setcacheresults(result)

    return result
