[![Travis build status](https://travis-ci.org/badele/domolib.png?branch=master)](https://travis-ci.org/badele/domolib) [![Coveralls status](https://coveralls.io/repos/badele/domolib/badge.png)](https://coveralls.io/r/badele/domolib)

sample
======

 - domolib -c "domolib.plugins.weather.sunshine.get_sunshineinfo('43:36:43', '3:53:38', '8')"
 - domolib -c "domolib.plugins.weather.sunshine.get_sunshineinfo('43:36:43', '3:53:38', '8')" -s "result['sun_alt']" 

 - domolib -c "domolib.plugins.weather.dlmetar.get_metarinfo('LFMT')"
 - domolib -c "domolib.plugins.weather.dlmetar.get_metarinfo('LFMT')" -s "result['temp']"


domolib
=======

Home automation library

- metar (temp, dewpt, pressure, visibility, wind_speed, humidity, wind_chill)
- vigilance (weatherlevelrisk, weatherrisk, floodlevelrisk)
- sunshine (selected_time_ts, sun_alt, sun_az, sunshine_idx,
            sunrise_std_ts, sunrise_civ_ts, sunrise_nav_ts, sunrise_ast_ts,
            sunset_std_ts, sunset_civ_ts, sunset_nav_ts, sunset_ast_ts)
- openweathermap (clouds, deg, humidity, pressure, speed, temp, weather, [rain])