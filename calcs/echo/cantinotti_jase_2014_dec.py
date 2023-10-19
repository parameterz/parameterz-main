#  !/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Haycock'
constraints = {'age': [0, 17], 'bsa':[0.12, 1.8]}

name = 'Cantinotti et al., JASE 2014, Dec'
description = 'BSA-adjusted z-scores of pediatric echo chamber diameters and areas.'

detail = '''Pediatric echo z-scores of the left atrium, left ventricle, right atrium, and right ventricle; chamber diameters and areas (but not volumes).
> ...this work substantially covers the gap of knowledge on chamber dimensions in children with the advantage of a rigorous statistical design.

'''
critique ={
  'model': 'exponential, and square root models with BSA',
  'subjects': 1091,
  'heterosc': True,
  'residual_assoc': True,
  'residual_heterosc': True,
  'distribution': True,
  'source': 'parameterz'
}
year = '2014'
citation = {
    'title': '''Echocardiographic nomograms for chamber diameters and areas in caucasian children.''',
    'authors': '''Cantinotti M, Scalese M, Murzi B, Assanta N, Spadoni I, De Lucia V, Crocetti M, Cresti A, Gallotta M, Marotta M, Tyack K, Molinaro S, Iervasi G.''',
    'journal': 'J Am Soc Echocardiogr. 2014 Dec;27(12):1279-1292.e2.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/25240494'
}

class Base(object):
    '''
    This is the base class for the Cantinotti data:
    '''

    def __init__( self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.refName = 'cantinotti_jase_2014_dec'
        self.siteName = data['name']
        self.eqnType = data['eqnType']
        self.slope = data['slope']
        self.intercept = data['intercept']
        self.rmse = data['rmse']
        self.limit = limit
        self.bsaMethod = bsaMethod
        self.bsa = pt.bsa(bsaMethod) 
        self.score = float(getattr(pt, data['name'])) 
        #chart stuff
        self.chartData = True
        self.bsaData = [x * 0.1 for x in range(1, 7)] #bsa range is 0.12-0.67
        self.chartXAxisLabel = 'BSA'
        self.myData = ( [[self.bsa, self.score]] )#plot data
        self.constraints = constraints
        self.critique = critique

    def _mean(self):
        if self.eqnType == 'exponential':
            return self.intercept + self.slope * math.log(self.bsa)
        elif self.eqnType == 'squareroot':
            return self.intercept + self.slope * math.sqrt(self.bsa)
    
    def mean(self):
        #returns the natural(back-transformed) mean value
        if self.eqnType == 'exponential':
            return math.exp(self._mean())
        elif self.eqnType == 'squareroot':
            return math.pow(self._mean(), 2)
    
    def zscore(self):
        if self.eqnType == 'exponential':
            return (math.log(self.score) - self._mean()) / self.rmse
        elif self.eqnType == 'squareroot':
            return (math.sqrt(self.score) - self._mean()) / self.rmse
    
    def uln(self):
        z = self.limit
        if self.eqnType == 'exponential':
            return math.exp(self._mean() + z * self.rmse)
        elif self.eqnType == 'squareroot':
            return math.pow(self._mean() + z * self.rmse ,2)
    
    def lln(self):
        z = self.limit
        if self.eqnType == 'exponential':
            return math.exp(self._mean() - z * self.rmse)
        elif self.eqnType == 'squareroot':
            return math.pow(self._mean() - z * self.rmse ,2)
# 
# individual site data 
#
lvedd_mm = { "name": "lvedd_mm", "eqnType": "exponential", "intercept": 3.634, "slope": 0.464, "rmse": 0.091 }
lvesd_mm = { "name": "lvesd_mm", "eqnType": "exponential", "intercept": 3.134, "slope": 0.459, "rmse": 0.137 }
la_major_a4c = { "name": "la_major_a4c", "eqnType": "exponential", "intercept": 3.492, "slope": 0.453, "rmse": 0.102 }
la_minor_a4c = { "name": "la_minor_a4c", "eqnType": "exponential", "intercept": 3.402, "slope": 0.454, "rmse": 0.095 }
la_area_a4c = { "name": "la_area_a4c", "eqnType": "exponential", "intercept": 2.191, "slope": 0.894, "rmse": 0.165 }
rv_len = { "name": "rv_len", "eqnType": "exponential", "intercept": 3.934, "slope": 0.484, "rmse": 0.098 }
rv_len_es = { "name": "rv_len_es", "eqnType": "squareroot", "intercept": 2.3744, "slope": 3.307, "rmse": 0.341 }
rv_b_a4c = { "name": "rv_b_a4c", "eqnType": "exponential", "intercept": 3.445, "slope": 0.499, "rmse": 0.113 }
rv_mc_a4c = { "name": "rv_mc_a4c", "eqnType": "exponential", "intercept": 3.048, "slope": 0.461, "rmse": 0.137 }
rv_eda_a4c = { "name": "rv_eda_a4c", "eqnType": "exponential", "intercept": 2.443, "slope": 0.955, "rmse": 0.171 }
rv_esa_a4c = { "name": "rv_esa_a4c", "eqnType": "exponential", "intercept": 1.542, "slope": 1.019, "rmse": 0.241 }
ra_major_a4c = { "name": "ra_major_a4c", "eqnType": "exponential", "intercept": 3.528, "slope": 0.474, "rmse": 0.101 }
ra_minor_a4c = { "name": "ra_minor_a4c", "eqnType": "exponential", "intercept": 3.450, "slope": 0.478, "rmse": 0.105 }
ra_area_a4c = { "name": "ra_area_a4c", "eqnType": "exponential", "intercept": 2.235, "slope": 0.911, "rmse": 0.178 }
lv_maj_ed_a4c = { "name": "lv_maj_ed_a4c", "eqnType": "exponential", "intercept": 4.099, "slope": 0.469, "rmse": 0.077 }
lv_maj_es_a4c = { "name": "lv_maj_es_a4c", "eqnType": "exponential", "intercept": 3.778, "slope": 0.506, "rmse": 0.106 }
lv_eda_a4c = { "name": "lv_eda_a4c", "eqnType": "exponential", "intercept": 2.924, "slope": 0.946, "rmse": 0.132 }
lv_esa_a4c = { "name": "lv_esa_a4c", "eqnType": "exponential", "intercept": 2.220, "slope": 0.975, "rmse": 0.183 }
lv_maj_ed_a2c = { "name": "lv_maj_ed_a2c", "eqnType": "exponential", "intercept": 4.097, "slope": 0.474, "rmse": 0.077 }
lv_maj_es_a2c = { "name": "lv_maj_es_a2c", "eqnType": "exponential", "intercept": 3.781, "slope": 0.504, "rmse": 0.106 }
lv_eda_a2c = { "name": "lv_eda_a2c", "eqnType": "exponential", "intercept": 2.923, "slope": 0.934, "rmse": 0.128 }
lv_esa_a2c = { "name": "lv_esa_a2c", "eqnType": "exponential", "intercept": 2.211, "slope": 0.983, "rmse": 0.179 }

sites = [

    'lvedd_mm',
    'lvesd_mm',
    'rv_len',
    'rv_len_es',
    'rv_b_a4c',
    'rv_mc_a4c',
    'rv_eda_a4c',
    'rv_esa_a4c',
    'ra_major_a4c',
    'ra_minor_a4c',
    'ra_area_a4c',
    'la_major_a4c',
    'la_minor_a4c',
    'la_area_a4c',
    'lv_maj_ed_a4c',
    'lv_maj_es_a4c',
    'lv_maj_ed_a2c',
    'lv_maj_es_a2c',
    'lv_eda_a4c',
    'lv_esa_a4c',
    'lv_eda_a2c',
    'lv_esa_a2c'    

]

