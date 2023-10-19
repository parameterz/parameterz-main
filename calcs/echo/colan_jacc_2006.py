#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Haycock'
constraints = {'age': [0, 18], 'bsa': [0, 2.0]}

name = 'Colan et al., JACC 2006'
description = 'BSA-adjusted z-scores for the aortic valve and sinuses.'

detail = '''Use this calculator to determine BSA-adjusted z-scores for
the aortic valve and aortic root (sinus of Valsalva), using
data from Boston Children's Hospital. 
'''

critique= {
  'model': 'linear with square root of BSA (allometric model)',
  'subjects': 'N/A',
  'heterosc': False,
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': False,
  'source': 'parameterz'
}

year = '2006'
citation = {
    'title': '''Validation and re-evaluation of a discriminant model 
    predicting anatomic suitability for biventricular repair in 
    neonates with aortic stenosis.''',
    'authors': 'Colan SD, McElhinney DB, Crawford EC, Keane JF, Lock JE.',
    'journal': 'J Am Coll Cardiol. 2006 May 2;47(9):1858-65.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/16682313'
}

class Base(object):
    '''
    This is the base class for the Boston AO Root.
        The form of these equations is:
            y = m*x + b
            where x = BSA^0.5
    '''

    def __init__(self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.siteName = data['name']
        self.refName = 'colan_jacc_2006'
        self.slope = data['slope']
        self.intercept = data['intercept']
        self.sd_slope = data['sd_slope']
        self.sd_intercept = data['sd_intercept']
        self.limit = limit
        self.bsaMethod = bsaMethod
        self.bsa = pt.bsa(bsaMethod)
        self.score = float(getattr(pt, data['name']))
        self.chartData = 'data=%s,%s' % (self.bsa, self.score) #plot data
        #chart stuff
        self.chartData = True
        self.bsaData = [x * 0.1 for x in range(1, 21)]
        self.chartXAxisLabel = 'BSA'
        self.constraints = constraints
        self.critique = critique

    def _mean(self, bsa):
        return self.slope * math.pow( bsa, 0.5 ) + self.intercept
        
    def mean(self):
        return 10 * self._mean(self.bsa)
    
    def sd(self, bsa):
        return self.sd_intercept + self.sd_slope * bsa
    
    def zscore(self):
        try:
            return (self.score/10 - self._mean(self.bsa)) / self.sd(self.bsa) #convert score to 'cm'
        except:
            return None #property of object 'pt' does not exist
    
    def uln(self):
        return ( (self._mean(self.bsa)) + self.limit * self.sd(self.bsa) ) * 10
    
    def lln(self):
        return ( (self._mean(self.bsa)) - self.limit * self.sd(self.bsa) ) * 10

    def chart_uln(self):
        return ( [[x, 10 * ( self.limit * self.sd(x) + self._mean(x) )] for x in self.bsaData] )
    def chart_lln(self):
        return ( [[x, 10 * ( -self.limit * self.sd(x) + self._mean(x) )] for x in self.bsaData] )
# 
# individual site data 
#

aov = { 'name': 'aov', 'slope': 1.55, 'intercept': 0, 'sd_slope': 0.083, 'sd_intercept': 0.06} 
sov = { 'name': 'sov', 'slope': 2.02, 'intercept': 0, 'sd_slope': 0.12, 'sd_intercept': 0.098}


sites = [
    'aov',
    'sov'    
    ]

