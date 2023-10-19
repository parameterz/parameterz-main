#  !/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Haycock'
constraints = {'age': [1.3, '18y'], 'BSA': [0.43, 2.2]}

name = 'Dallaire et al., Circ Cardiovasc Imaging 2015'
description = 'BSA-adjusted z-scores for inflow and tissue Doppler of the left heart'

detail = '''BSA-adjusted z-scores for left-sided pulse wave Doppler and tissue Doppler imaging routinely used in a clinical setting.

>As Z scores describe the normal limit of a healthy population, other studies are needed to further
define the threshold above which health becomes a disease by integrating other important factors
such as ventricular morphology, loading condition, and HR.

Note: this is a work-in-progress; there are 13 PW and 14 TD measures... these are the most common. Others will get rolled out as time allows.
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
year = '2015'
citation = {
    'title': 'Reference values for pulse wave Doppler and tissue Doppler imaging in pediatric echocardiography.',
    'authors': 'Dallaire F, Slorach C, Hui W, Sarkola T, Friedberg MK, Bradley TJ, Jaeggi E, Dragulescu A, Har RL, Cherney DZ, Mertens L.',
    'journal': 'Circ Cardiovasc Imaging. 2015 Feb;8(2). ',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/25632029'
}

class Base(object):
    '''
    This is the base class for the Dallaire Doppler data.
    There are several forms of these equations, ...
    '''

    def __init__( self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.refName = 'dallaire_circimaging_2015'
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

    
    def mean(self):
        ### Untransformed values ###
        if self.eqnType == 'linear': 
            return self.values['c'] * self.bsa + self.values['d']
        if self.eqnType == 'poly-2': 
            return self.values['b'] * math.pow(self.bsa, 2) + self.values['c'] * self.bsa + self.values['d'] 
        if self.eqnType == 'poly-3': 
            return self.values['a'] * math.pow(self.bsa, 3) + self.values['b'] * math.pow(self.bsa, 2) + self.values['c'] * self.bsa + self.values['d']
        if self.eqnType == 'allometric': 
            return self.values['e'] * math.pow(self.bsa, self.values['f'])
        ### Transformed values ###
        if self.eqnType in ['log-linear', 'log-allometric']:
            return math.exp( self._mean() )
    
    def sd(self):
        # all sd's are calculated the same way, regardless of eqnType
        # g * BSA + h
        g = self.values['g']
        h = self.values['h']
        return g * self.bsa + h
    
    def zscore(self):
        if self.eqnType in ['linear', 'poly-2', 'poly-3', 'allometric']: #no transformation necessary; can return simple, untransformed value
            return ( self.score - self.mean() ) / self.sd()
        if self.eqnType in ['log-linear', 'log-allometric']:
            return ( math.log( self.score ) - self._mean() ) / self.sd()
    
    def uln(self):
        z = self.limit
        if self.eqnType in ['linear', 'poly-2', 'poly-3', 'allometric']: #can return simple, untransformed value
            return self.mean() + z * self.sd()
        if self.eqnType in ['log-linear', 'log-allometric']:
            return math.exp( self._mean() + z * self.sd() )
    
    def lln(self):
        z = self.limit
        if self.eqnType in ['linear', 'poly-2', 'poly-3', 'allometric']: #can return simple, untransformed value
            return self.mean() - z * self.sd()
        if self.eqnType in ['log-linear', 'log-allometric']:
            return math.exp( self._mean() - z * self.sd() )
        
# 
# individual site data 
# 


mv_e = { 'name': 'mv_e', 'eqnType': 'poly-3', 'values': { 'a': 5.363, 'b': -16.239, 'c': 0.728, 'd': 116.202, 'g': 3.038, 'h': 11.166 } }
mv_a = { 'name': 'mv_a', 'eqnType': 'log-allometric', 'values': { 'e': 3.873, 'f': -0.1115, 'g': 0.038, 'h': 0.199 } }
mv_ea_ratio = { 'name': 'mv_ea_ratio', 'eqnType': 'log-allometric', 'values': { 'e': 0.770, 'f': 0.3015, 'g': 0.028, 'h': 0.234 } }
lv_tdi_e = { 'name': 'lv_tdi_e', 'eqnType': 'poly-3', 'values': { 'a': 7.343, 'b': -31.380, 'c': 42.148, 'd': 1.463, 'g': -0.500, 'h': 3.071  } }
lv_tdi_a = { 'name': 'lv_tdi_a', 'eqnType': 'log-linear', 'values': { 'c': -0.029, 'd': 1.831, 'g': 0.044, 'h': 0.179 } }
lv_tdi_s = { 'name': 'lv_tdi_s', 'eqnType': 'poly-3', 'values': { 'a': 4.631, 'b': -18.272, 'c': 24.964, 'd': -1.064, 'g': 0.163, 'h': 1.605 } }
septal_tdi_e = { 'name': 'septal_tdi_e', 'eqnType': 'poly-3', 'values': { 'a': 2.506, 'b': -11.701, 'c': 17.341, 'd': 7.290, 'g': 0.141, 'h': 2.014 } }
septal_tdi_a = { 'name': 'septal_tdi_a', 'eqnType': 'log-linear', 'values': { 'c': -0.031, 'd': 1.827, 'g': 0.047, 'h': 0.142 } }
septal_tdi_s  = { 'name': 'septal_tdi_s', 'eqnType': 'poly-3', 'values': { 'a': 2.004, 'b': -7.375, 'c': 8.982, 'd': 4.856, 'g': -0.028, 'h': 0.840 } }


sites = [
    
    'mv_e',
    'mv_a',
    'mv_ea_ratio',
    'lv_tdi_e',
    'lv_tdi_a',
    'lv_tdi_s',
    'septal_tdi_e',
    'septal_tdi_a',
    'septal_tdi_s'
    
]
