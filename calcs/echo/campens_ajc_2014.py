#!/usr/bin/env python
from __future__ import division
import math

required = ['bsa', 'gender', 'age']
bsaMethod = 'Haycock' #article sources both Haycock and Dubois with no sig diff's; going with Haycock
name = 'Campens et al., Am J Cardiol 2014'
year = '2014'
description = 'Age, BSA, and gender adjusted reference values for the sinus of Valsalva and ascending aorta.'

detail ='''A gender-specific multivariate model with age and BSA; developed using a large cohort of children and adults, ranging from 1 to 85 years.
>We demonstrate that age, body size, and gender are strong independent predictors of proximal aortic diameters.

(Note that vessel diameters are measured in _diastole_.)
'''

critique = {
  'model': 'multiple regression with height, weight, age, and gender',
  'subjects': 849,
  'heterosc': False,
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': False,
  'source': 'parameterz'
}
citation = {
    'title': 'Reference values for echocardiographic assessment of the diameter of the aortic root and ascending aorta spanning all age categories.',
    'authors': 'Campens L, Demulier L, De Groote K, Vandekerckhove K, De Wolf D, Roman MJ, Devereux RB, De Paepe A, De Backer J.',
    'journal': 'Am J Cardiol. 2014 Sep 15;114(6):914-20.',
    'year': '2014',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/25092193'
}
constraints = {'age': [1, 85] }

class Base(object):
    '''Base class for Campens z-scores'''
    def __init__(self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.siteName = data['name']
        self.refName = 'campens_ajc_2014'
        self.wt = float(pt.wt)
        self.ht = float(pt.ht)
        self.bsaMethod = bsaMethod
        self.bsa = pt.bsa(bsaMethod) 
        self.gender = pt.gender
        self.age = float(pt.age)
        self.score = float(getattr(pt, data['name']))
        self.data = data['female'] if pt.gender == 'f' else data['male']
        self.limit = limit
        #chart stuff
        self.chartData = False
        self.constraints = constraints
        self.critique = critique
        
    def _mean(self):
        return ( self.data['a1'] + self.data['b1'] * math.log10( self.age ) ) + self.data['a2'] * self.bsa
        
    def mean(self):
        return math.pow( 10, self._mean() )
    
    def zscore(self):
        try:
            return ( math.log10( self.score ) - self._mean() ) / self.data['see']
        except:
            return None
    
    def lln(self):
        z = self.limit
        return math.pow( 10, self._mean() - (z * self.data['see']) )

    def uln(self):
        z = self.limit
        return math.pow( 10, self._mean() + (z * self.data['see']) )

# 
# individual site data
#
#2D
sov_d = {'name': 'sov_d', 
         'male': { 'a1': 1.115, 'b1': 0.137, 'a2': 0.094, 'see': 0.0388 }, 
         'female': { 'a1':  1.112, 'b1': 0.132, 'a2': 0.080, 'see':0.0427 }
        }
aao_d = {'name': 'aao_d', 
         'male': { 'a1': 1.038, 'b1': 0.187, 'a2': 0.068, 'see': 0.0433 }, 
         'female': { 'a1': 1.006, 'b1': 0.172, 'a2': 0.087, 'see': 0.0450 }
        }


sites = [
    'sov_d',
    'aao_d'
]
