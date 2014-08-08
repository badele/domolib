#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import ephem
import math


class sunshine():
    """Check if day or night"""

    def getresults(self, **params):

        results = {}

        # Location
        if 'latitude' not in params:
            raise Exception('Please set the latitude parameter')

        if 'longitude' not in params:
            raise Exception('Please set the longitude parameter')

        # Elevation
        if 'elevation' not in params:
            params['elevation'] = 0

        # Consts
        HORIZON_STANDARD = "-0.833"
        HORIZON_CIVIL = "-6"
        HORIZON_NAVAL = "-12"
        HORIZON_ASTRO = "-18"

        # Select datetime
        if 'datetime' not in params:
            pdate = ephem.now()
            results['selected_time'] = ephem.localtime(pdate)
        else:
            pdate = ephem.Date(params['datetime'])
            results['selected_time'] = pdate

        results['selected_time_ts'] = int(time.mktime(pdate.datetime().timetuple()))

        # Observer horizon
        if 'horizon_std' not in params:
            params['horizon_std'] = HORIZON_STANDARD

        if 'horizon_civ' not in params:
            params['horizon_civ'] = HORIZON_CIVIL

        if 'horizon_nav' not in params:
            params['horizon_nav'] = HORIZON_NAVAL

        if 'horizon_ast' not in params:
            params['horizon_ast'] = HORIZON_ASTRO

        # Observer details
        obs = ephem.Observer()
        obs.lat = params['latitude']
        obs.long = params['longitude']
        obs.elevation = int(params['elevation'])
        obs.date = pdate

        # The sun
        sun = ephem.Sun(obs)
        sun.compute(obs)

        # Sun position
        results['sun_alt'] = int(sun.alt * 180 / math.pi)
        results['sun_az'] = int(sun.az * 180 / math.pi)

        # Calc transit sun
        nexttransit = obs.next_transit(sun)
        prevtransit = obs.previous_transit(sun)

        if pdate.datetime().date() == nexttransit.datetime().date():
            obs.date = nexttransit

        if pdate.datetime().date() == prevtransit.datetime().date():
            obs.date = prevtransit

        # Standard
        obs.horizon = params['horizon_std']
        sunrise_std = obs.previous_rising(sun)
        sunset_std  = obs.next_setting(sun)
        results['sunrise_std'] = ephem.localtime(sunrise_std)
        results['sunset_std']  = ephem.localtime(sunset_std)
        results['sunrise_std_ts'] = int(time.mktime(obs.previous_rising(sun).datetime().timetuple()))
        results['sunset_std_ts']  = int(time.mktime(obs.next_setting(sun).datetime().timetuple()))

        # Civil
        obs.horizon = params['horizon_civ']
        sunrise_civ = obs.previous_rising(sun)
        sunset_civ  = obs.next_setting(sun)
        results['sunrise_civ'] = ephem.localtime(sunrise_civ)
        results['sunset_civ']  = ephem.localtime(sunset_civ)
        results['sunrise_civ_ts'] = int(time.mktime(obs.previous_rising(sun).datetime().timetuple()))
        results['sunset_civ_ts']  = int(time.mktime(obs.next_setting(sun).datetime().timetuple()))

        # Nav
        obs.horizon = params['horizon_nav']
        sunrise_nav = obs.previous_rising(sun)
        sunset_nav  = obs.next_setting(sun)
        results['sunrise_nav'] = ephem.localtime(sunrise_nav)
        results['sunset_nav']  = ephem.localtime(sunset_nav)
        results['sunrise_nav_ts'] = int(time.mktime(obs.previous_rising(sun).datetime().timetuple()))
        results['sunset_nav_ts']  = int(time.mktime(obs.next_setting(sun).datetime().timetuple()))

        # Astro
        obs.horizon = params['horizon_ast']
        sunrise_ast = obs.previous_rising(sun)
        sunset_ast  = obs.next_setting(sun)
        results['sunrise_ast'] = ephem.localtime(sunrise_ast)
        results['sunset_ast']  = ephem.localtime(sunset_ast)
        results['sunrise_ast_ts'] = int(time.mktime(obs.previous_rising(sun).datetime().timetuple()))
        results['sunset_ast_ts']  = int(time.mktime(obs.next_setting(sun).datetime().timetuple()))

        idx = -1
        if pdate < sunrise_ast or pdate > sunset_ast:
            # Night
            idx = 0

        if idx < 0 and (
                (pdate > sunrise_ast and pdate < sunrise_nav)
                or
                (pdate > sunset_nav and pdate < sunset_ast)
        ):
            # Astronomic
            idx = 1

        if idx < 0 and (
                (pdate > sunrise_nav and pdate < sunrise_civ)
                or
                (pdate > sunset_civ and pdate < sunset_nav)
        ):
            # Naval
            idx = 2

        if idx < 0 and (
                (pdate > sunrise_civ and pdate < sunrise_std)
                or
                (pdate > sunset_std and pdate < sunset_civ)
        ):
            # Civil
            idx = 3

        if idx < 0 and pdate > sunrise_std and pdate < sunset_std:
            # Day
            idx = 255

        results['sunshine_idx'] = idx

        return results
