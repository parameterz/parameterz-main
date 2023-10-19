#!/usr/bin/env python

from __future__ import division
import math

required = ['wt']
bsaMethod = None
name = 'Overbeek et al., Eur J Echocardiogr 2006'
year = '2006'
description = 'Weight-adjusted M-Mode z-scores.'
detail = '''Weight-adjusted z-scores of left ventricular M-mode diameters.
Data is from over 700 Dutch children as described by investigators at
Children's Heart Centre, The Netherlands.
'''
critique = {
  'model': 'log-log model with weight',
  'subjects': 747,
  'heterosc': True,
  'residual_assoc': True,
  'residual_heterosc': True,
  'distribution': False
}

year = '2006'
citation = {
    'title': 'New reference values for echocardiographic dimensions of healthy Dutch children.',
    'authors': 'Overbeek LI, Kapusta L, Peer PG, de Korte CL, Thijssen JM, Daniels O.',
    'journal': 'Eur J Echocardiogr. 2006 Mar;7(2):113-21.',
    'year': '2006',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/15941671'
}
constraints = {'age': [0,18], 'wt': [2.5, 90]}


class Base(object):
    '''Base class for Overbeek m-mode z-scores'''
    def __init__(self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.siteName = data['name']
        self.refName = 'overbeek_eje_2006'
        self.limit = limit
        self.wt = float(pt.wt)
        self.score = float(getattr(pt, data['name']))
        self.intercept = data['intercept']
        self.slope = data['slope']
        self.sd = data['sd']
        #chart stuff
        self.chartData = True
        self.chartXAxisLabel = 'WT'
        self.myData = ( [[self.wt, self.score]] )#plot data
        self.constraints = constraints
        self.critique = critique

    def _mean(self, wt):
        if wt is None:
            wt = self.wt
        return self.intercept + math.log(wt) * self.slope
    
    def mean(self):
        return math.exp(self._mean(self.wt))
    
    def zscore(self):
        score = math.log(self.score)
        return ( score - self._mean(self.wt) ) / self.sd
    
    def lln(self):
        z = self.limit
        return math.exp(self._mean(self.wt) - z * self.sd)

    def uln(self):
        z = self.limit
        return math.exp(self._mean(self.wt) + z * self.sd)


# 
# individual site data 
#
ivsd_mm = {'name': 'ivsd_mm', 'intercept': 0.665, 'slope': 0.277, 'sd': 0.213}
lvedd_mm = {'name': 'lvedd_mm', 'intercept': 2.551, 'slope': 0.341, 'sd': 0.108}
lvpwd_mm = {'name': 'lvpwd_mm', 'intercept': 0.704, 'slope': 0.298, 'sd': 0.211}
lvesd_mm = {'name': 'lvesd_mm', 'intercept': 2.123, 'slope': 0.332, 'sd': 0.138}


sites = [
    'ivsd_mm',
    'lvedd_mm',
    'lvpwd_mm',
    'lvesd_mm'
]
