[![Travis build status](https://travis-ci.org/badele/domolib.png?branch=master)](https://travis-ci.org/badele/domolib) [![Coveralls status](https://coveralls.io/repos/badele/domolib/badge.png)](https://coveralls.io/r/badele/domolib)

# Domolib

Home automation library, this library expose the functions, this functions can also used from command line.

# Installation

``` bash
    $ pip install git+git://github.com/badele/domolib.git
```

# Sample

Get functions list

``` bash
    $ domolib -l
    #
    # + domolib.plugins.weather.sunshine
    # | get_sunshineinfo(latitude, longitude, elevation)  Get the sun position and sunshine
    #
    # + domolib.plugins.weather.dlmetar
    # | get_metarinfo(oaci_station)  Get a weather from metar report
    # 
    # + domolib.plugins.weather.vigimeteo
    # | get_vigimeteoinfo(department)  Get department flood alert
    #
    # + domolib.plugins.weather.openweathermap
    # | get_today_weather(latitude, longitude)     Get today weather
    # | get_tomorrow_weather(latitude, longitude)  Get tomorrow weather
```


Get weather informations in flat mode

``` bash
    $ domolib -c "domolib.plugins.weather.openweathermap.get_today_weather(43.61,3.88)"
    #
    # clouds             : 0
    # deg                : 99
    # dt                 : 1439290800
    # humidity           : 54
    # pressure           : 973.4
    # speed              : 1.47
    # temp.day           : 33.5
    # temp.eve           : 32.35
    # temp.max           : 34.84
    # temp.min           : 21.09
    # temp.morn          : 30
    # temp.night         : 21.09
    # weather.description: sky is clear
    # weather.icon       : 01d
    # weather.id         : 800
    # weather.main       : Clear
```

Get weather informations in json mode

``` bash
    $ domolib -c "domolib.plugins.weather.openweathermap.get_today_weather(43.61,3.88)" -f json
    # 
    # { u'clouds': 0,
    #   u'deg': 99,
    #   u'dt': 1439290800,
    #   u'humidity': 54,
    #   u'pressure': 973.4,
    #   u'speed': 1.47,
    #   u'temp': { u'day': 33.5,
    #              u'eve': 32.35,
    #              u'max': 34.84,
    #              u'min': 21.09,
    #              u'morn': 30,
    #              u'night': 21.09},
    #   u'weather': [ { u'description': u'sky is clear',
    #                   u'icon': u'01d',
    #                   u'id': 800,
    #                   u'main': u'Clear'}]}
```

Get weather informations and select the temp

``` bash
    $ domolib -c "domolib.plugins.weather.openweathermap.get_today_weather(43.61,3.88)" -s "result['temp']['day']"
    #
    # 33.5
```

Get metar informations

``` bash
    $ domolib -c "domolib.plugins.weather.dlmetar.get_metarinfo('LFMT')"
    #
    # dewpt     : 16.0
    # humidity  : 45.34
    # pressure  : 1014.0
    # temp      : 29.0
    # visibility: 10000
    # wind_chill: 31.32
    # wind_speed: 7.408
```

Get sunshine informations

``` bash
    $ domolib -c "domolib.plugins.weather.sunshine.get_sunshineinfo('43:36:43', '3:53:38', '8')"
    #
    # selected_time   : 2015-08-11 12:30:31.000001
    # selected_time_ts: 1439289031
    # sun_alt         : 57
    # sun_az          : 143
    # sunrise_ast     : 2015-08-11 04:48:26.000001
    # sunrise_ast_ts  : 1439261306
    # sunrise_civ     : 2015-08-11 06:10:08.000001
    # sunrise_civ_ts  : 1439266208
    # sunrise_nav     : 2015-08-11 05:31:46.000001
    # sunrise_nav_ts  : 1439263906
    # sunrise_std     : 2015-08-11 06:37:11.000001
    # sunrise_std_ts  : 1439267831
    # sunset_ast      : 2015-08-11 22:49:26.000001
    # sunset_ast_ts   : 1439326166
    # sunset_civ      : 2015-08-11 21:28:18.000001
    # sunset_civ_ts   : 1439321298
    # sunset_nav      : 2015-08-11 22:06:27.000001
    # sunset_nav_ts   : 1439323587
    # sunset_std      : 2015-08-11 21:01:22.000001
    # sunset_std_ts   : 1439319682
    # sunshine_idx    : 255
```

Get french department flood alert

``` bash
    $ domolib -c "domolib.plugins.weather.vigimeteo.get_vigimeteoinfo('34')"
    #
    # floodlevelrisk  : green
    # risk            : RAS
    # weatherlevelrisk: green
```
