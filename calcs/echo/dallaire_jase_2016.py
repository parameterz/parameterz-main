#  !/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Haycock'
constraints = {'age': [1.3, '18y'], 'BSA': [0.43, 2.2]}

name = 'Dallaire et al., JASE 2016'
description = 'BSA-adjusted z-scores for left ventricular strain; normal values for pediatric longitudinal and circumferential strain'

detail = '''BSA-adjusted z-scores for longitudinal and circumferential strain for pediatric patients.

>These Z scores will help reduce the confounding effect of body size in strain measurements,
which should ease their clinical interpretation in pediatric echocardiography.

Note: Because of poor reproducibility and vendor-specific effects, the authors elected to exclude radial strain measurements from this study.

Also note:

>To compute Z score equations that would yield intuitively lower Z scores for
measurements closer to zero, we used the **absolute value** of strain
measurements with negative values. 

'''

critique ={
  'model': 'tba',
  'subjects': 233,
  'heterosc': True,
  'residual_assoc': True,
  'residual_heterosc': True,
  'distribution': True,
  'source': 'source article'
}
year = '2016'
citation = {
    'title': 'Pediatric Reference Values and Z Score Equations for Left Ventricular Systolic Strain Measured by Two-Dimensional Speckle-Tracking Echocardiography.',
    'authors': 'Dallaire F, Slorach C, Bradley T, Hui W, Sarkola T, Friedberg MK, Jaeggi E, Dragulescu A, Mahmud FH, Daneman D, Mertens L.',
    'journal': 'J Am Soc Echocardiogr. 2016 May 13. ',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/27185223'
}

class Base(object):
    '''
    This is the base class for the Dallaire strain data.
    There are several forms of these equations, ...
    '''

    def __init__( self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.refName = 'dallaire_jase_2016'
        self.siteName = data['name']
        self.bsaMethod = bsaMethod
        self.bsa = pt.bsa(bsaMethod)
        self.eqnType = data['eqnType']
        self.values = data['values'] 
        self.limit = limit
        self.score = float(getattr(pt, data['name']))
        #chart stuff
        self.chartData = False
        #self.bsaData = [x * 0.1 for x in range(1, 7)] #bsa range is 0.12-0.67
        #self.chartXAxisLabel = 'BSA'
        #self.myData = ( [[self.bsa, self.score]] )#plot data
        self.constraints = constraints
        self.critique = critique


    
    def _mean(self):
        #returns the untransformed mean value 
        if self.eqnType == 'log-linear':
            return self.values['c'] * self.bsa + self.values['d']
        if self.eqnType == 'log-allometric':
            return self.values['e'] * math.pow( self.bsa, self.values['f'] )
        if self.eqnType in [ 'recip-poly', 'log-poly']:
            return self.values['a'] * math.pow(self.bsa, 2) + self.values['b'] * self.bsa + self.values['c']


    
    def mean(self):
        ### Untransformed values ###
        if self.eqnType == 'linear': 
            return self.values['c'] * self.bsa + self.values['d']
        if self.eqnType == 'poly-2': 
            return self.values['a'] * math.pow(self.bsa, 2) + self.values['b'] * self.bsa + self.values['c'] 
        if self.eqnType == 'poly-3': 
            return self.values['a'] * math.pow(self.bsa, 3) + self.values['b'] * math.pow(self.bsa, 2) + self.values['c'] * self.bsa + self.values['d']
        if self.eqnType == 'allometric': 
            return self.values['d'] * math.pow(self.bsa, self.values['e'])
        ### Transformed values ###
        if self.eqnType in ['log-linear', 'log-allometric', 'log-poly']:
            return math.exp( self._mean() )
        if self.eqnType == 'recip-poly':
            return 1 / self._mean()
    
    def sd(self):
        # all sd's are calculated the same way, regardless of eqnType
        # f * BSA + g
        f = self.values['f']
        g = self.values['g']
        return f * self.bsa + g
    
    def zscore(self):
        if self.eqnType in ['linear', 'poly-2', 'poly-3', 'allometric']: #no transformation necessary; can return simple, untransformed value
            return ( self.score - self.mean() ) / self.sd()
        if self.eqnType in ['log-linear', 'log-allometric', 'log-poly']:
            return ( math.log( self.score ) - self._mean() ) / self.sd()
        if self.eqnType == 'recip-poly':
            return -1 * ( (1 / self.score) - self._mean() ) / self.sd() #reciprocal function yields opposite result
    
    def uln(self):
        z = self.limit
        if self.eqnType in ['linear', 'poly-2', 'poly-3', 'allometric']: #can return simple, untransformed value
            return self.mean() + z * self.sd()
        if self.eqnType in ['log-linear', 'log-allometric', 'log-poly']:
            return math.exp( self._mean() + z * self.sd() )
        if self.eqnType == 'recip-poly':
            limit = self._mean() - z * self.sd() #reciprocal function yields opposite result
            return 1 / limit
    
    def lln(self):
        z = self.limit
        if self.eqnType in ['linear', 'poly-2', 'poly-3', 'allometric']: #can return simple, untransformed value
            return self.mean() - z * self.sd()
        if self.eqnType in ['log-linear', 'log-allometric', 'log-poly']:
            return math.exp( self._mean() - z * self.sd() )
        if self.eqnType == 'recip-poly':
            limit = self._mean() + z * self.sd() #reciprocal function yields opposite result
            return 1 / limit        
# 
# individual site data 
# 


mean_ls = { 'name': 'mean_ls', 'eqnType': 'allometric', 'values': { 'd': 20.295, 'e': -0.0614, 'f': -0.343, 'g': 2.02 } }
basal_mean_cs = { 'name': 'basal_mean_cs', 'eqnType': 'poly-2', 'values': { 'a': -1.218, 'b': 2.428, 'c': 18.93, 'f': 0.158, 'g': 1.64 } }
mid_mean_cs = { 'name': 'mid_mean_cs', 'eqnType': 'recip-poly', 'values': { 'a': 0.000665, 'b': 0.0000300, 'c': 0.0509, 'f': 0.000437, 'g': 0.00380 } }
apical_mean_cs = { 'name': 'apical_mean_cs', 'eqnType': 'log-poly', 'values': { 'a': -0.0128, 'b': 0.0320, 'c': 2.935, 'f': 0.00238, 'g': 0.104 } }


sites = [
    
    'mean_ls',
    'basal_mean_cs',
    'mid_mean_cs',
    'apical_mean_cs'
    
    
]
