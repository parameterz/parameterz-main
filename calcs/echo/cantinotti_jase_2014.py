#  !/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Haycock'
constraints = {'age': [0, 3], 'bsa':[0.12, 0.67]}

name = 'Cantinotti et al., JASE 2014'
description = 'BSA-adjusted cardiac z-scores for infants and children.'

detail = '''BSA-adjusted Z scores derived from a large population of Caucasian
neonates, infants, and toddlers calculated using "_a rigorous statistical design"_:
particular attention was paid to matters of skew/distribution and heteroscedasticity.

'''
critique ={
  'model': 'linear, exponential, and square root models with BSA',
  'subjects': 445,
  'heterosc': True,
  'residual_assoc': True,
  'residual_heterosc': True,
  'distribution': True,
  'source': 'parameterz'
}
year = '2014'
citation = {
    'title': '''Echocardiographic Nomograms for Ventricular, Valvular and
    Arterial Dimensions in Caucasian Children with a Special Focus on Neonates,
    Infants and Toddlers.''',
    'authors': '''Cantinotti M, Scalese M, Murzi B, Assanta N, Spadoni I,
    Festa P, De Lucia V, Maura C, Marco M, Molinaro S, Lopez L, Iervasi G.''',
    'journal': 'J Am Soc Echocardiogr. 2014 Feb;27(2):179-191.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/24316257'
}

class Base(object):
    '''
    This is the base class for the Cantinotti data:
    '''

    def __init__( self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.refName = 'cantinotti_jase_2014'
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
        if self.eqnType == 'linear':
            return (self.intercept + self.slope * self.bsa)
        elif self.eqnType == 'exponential':
            return math.exp(self._mean())
        elif self.eqnType == 'squareroot':
            return math.pow(self._mean(), 2)
    
    def zscore(self):
        if self.eqnType == 'linear':
            return ( self.score - self.mean()) / self.rmse
        elif self.eqnType == 'exponential':
            return (math.log(self.score) - self._mean()) / self.rmse
        elif self.eqnType == 'squareroot':
            return (math.sqrt(self.score) - self._mean()) / self.rmse
    
    def uln(self):
        z = self.limit
        if self.eqnType == 'linear':
            return self.mean() + z * self.rmse
        elif self.eqnType == 'exponential':
            return math.exp(self._mean() + z * self.rmse)
        elif self.eqnType == 'squareroot':
            return math.pow(self._mean() + z * self.rmse ,2)
    
    def lln(self):
        z = self.limit
        if self.eqnType == 'linear':
            return self.mean() - z * self.rmse
        elif self.eqnType == 'exponential':
            return math.exp(self._mean() - z * self.rmse)
        elif self.eqnType == 'squareroot':
            return math.pow(self._mean() - z * self.rmse ,2)
# 
# individual site data 
#
ivc = { "name": "ivc", "eqnType": "exponential", "intercept": 2.096, "slope": 0.607, "rmse": 0.237 }
tvd_l = { "name": "tvd_l", "eqnType": "exponential", "intercept": 3.139, "slope": 0.43, "rmse": 0.1 }
pv = { "name": "pv", "eqnType": "exponential", "intercept": 2.911, "slope": 0.539, "rmse": 0.107 }
mpa = { "name": "mpa", "eqnType": "squareroot", "intercept": 1.637, "slope": 2.937, "rmse": 0.186 }
rpa = { "name": "rpa", "eqnType": "exponential", "intercept": 2.52, "slope": 0.658, "rmse": 0.149 }
lpa = { "name": "lpa", "eqnType": "squareroot", "intercept": 0.839, "slope": 2.725, "rmse": 0.188 }
mvd_l = { "name": "mvd_l", "eqnType": "squareroot", "intercept": 1.953, "slope": 3.08, "rmse": 0.164 }
aov = { 'name': 'aov', 'eqnType': 'exponential', 'intercept': 2.804, 'slope': 0.561, 'rmse': 0.085 }
sov = { "name": "sov", "eqnType": "exponential", "intercept": 3.057, "slope": 0.49, "rmse": 0.092 }
stj = { "name": "stj", "eqnType": "exponential", "intercept": 2.808, "slope": 0.529, "rmse": 0.096 }
aao = { "name": "aao", "eqnType": "exponential", "intercept": 2.921, "slope": 0.465, "rmse": 0.095 }
prox_arch = { "name": "prox_arch", "eqnType": "exponential", "intercept": 2.721, "slope": 0.497, "rmse": 0.121 }
mid_arch = { "name": "mid_arch", "eqnType": "exponential", "intercept": 2.55, "slope": 0.5, "rmse": 0.122 }
dist_arch = { "name": "dist_arch", "eqnType": "exponential", "intercept": 2.513, "slope": 0.541, "rmse": 0.125 }
isthmus = { "name": "isthmus", "eqnType": "exponential", "intercept": 2.454, "slope": 0.628, "rmse": 0.146 }
dao = { "name": "dao", "eqnType": "exponential", "intercept": 2.547, "slope": 0.517, "rmse": 0.127 }
abd_ao = { "name": "abd_ao", "eqnType": "linear", "intercept": 3.45, "slope": 7.938, "rmse": 0.749 }
ivsd_mm = { "name": "ivsd_mm", "eqnType": "squareroot", "intercept": 1.106, "slope": 1.689, "rmse": 0.188 }
lvedd_mm = { "name": "lvedd_mm", "eqnType": "squareroot", "intercept": 2.424, "slope": 4.021, "rmse": 0.21 }
lvpwd_mm = { "name": "lvpwd_mm", "eqnType": "exponential", "intercept": 1.842, "slope": 0.471, "rmse": 0.181 }
lvesd_mm = { "name": "lvesd_mm", "eqnType": "linear", "intercept": 7.577, "slope": 17.97, "rmse": 1.782 }
lvm_mm = { "name": "lvm_mm", "eqnType": "squareroot", "intercept": -1.279, "slope": 9.107, "rmse": 0.407 }

sites = [
    'ivc',
    'tvd_l',
    'pv',
    'mpa',
    'rpa',
    'lpa',
    'mvd_l',
    'aov',
    'sov',
    'stj',
    'aao',
    'prox_arch',
    'mid_arch',
    'dist_arch',
    'isthmus',
    'dao',
    'abd_ao',
    'ivsd_mm',
    'lvedd_mm',
    'lvpwd_mm',
    'lvesd_mm',
    'lvm_mm'
]

