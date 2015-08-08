#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

from xml.dom import minidom


class vigimeteo:
        def __init__(self, **params):

            # Set parameters
            self.params = params
            self.results = {}

        def getvigilance(self, deprequest):
            if len(deprequest) != 2:
                raise Exception("Error in department number")

            url = 'http://vigilance.meteofrance.com/data/NXFR34_LFPW_.xml'
            dom = minidom.parse(urlopen(url))

            colors = ['green', 'green', 'yellow', 'orange', 'red']
            risks = ['NONE', 'wind', 'flooding rain', 'storm', 'flooding', 'snow ice', 'cold']

            for all in dom.getElementsByTagName('datavigilance'):
                depart = all.attributes['dep'].value

                riskid = -1
                floodid = -1
                for risk in all.getElementsByTagName('risque'):
                    riskid = int(risk.attributes['valeur'].value)
                for flood in all.getElementsByTagName('crue'):
                    floodid = int(flood.attributes['valeur'].value)

                colorresult = int(all.attributes['couleur'].value)
                floodresult = colors[floodid]
                if riskid != -1:
                    riskresult = risks[riskid]
                else:
                    riskresult = "RAS"

                if depart == deprequest:
                    color = colors[colorresult]
                    return {
                        'weatherlevelrisk': color,
                        'risk': riskresult,
                        'floodlevelrisk': floodresult
                    }

            return None
