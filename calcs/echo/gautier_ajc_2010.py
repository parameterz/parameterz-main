#!/usr/bin/env python
from __future__ import division
import math

required = ['bsa', 'gender']
bsaMethod = 'Dubois' 
name = 'Gautier et al., Am J Cardiol 2010'
year = '2010'
description = 'BSA, and gender adjusted reference values for the aortic valve and aortic root in children.'

detail ='''Linear regression statistics were 
applied to determine the correlations among the logarithmic
transformed values of the 4 aortic root diameters, morphologic
parameters, and age.

>normative data for the aortic root ... in children should be useful for diagnosis and
follow-up of various aneurismal pathologic disorders

(Note that vessel diameters are measured in _diastole_.)
'''

critique = {
  'model': 'gender-specific log/log regression with BSA',
  'subjects': 353,
  'heterosc': False,
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': False,
  'source': 'parameterz'
}
citation = {
    'title': 'Nomograms for aortic root diameters in children using two-dimensional echocardiography.',
    'authors': 'Gautier M, Detaint D, Fermanian C, Aegerter P, Delorme G, Arnoult F, Milleron O, Raoux F, Stheneur C, Boileau C, Vahanian A, Jondeau G.',
    'journal': 'Am J Cardiol. 2010 Mar 15;105(6):888-94',
    'year': '2010',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/20211339'
}
constraints = {'age': [2, 18] }

class Base(object):
    '''Base class for Gautier z-scores'''
    def __init__(self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.siteName = data['name']
        self.refName = 'gautier_ajc_2010'
        self.wt = float(pt.wt)
        self.ht = float(pt.ht)
        self.bsaMethod = bsaMethod
        self.bsa = pt.bsa(bsaMethod) 
        self.gender = pt.gender
        self.score = float(getattr(pt, data['name']))
        self.data = data['female'] if pt.gender == 'f' else data['male']
        self.limit = limit
        #chart stuff
        self.chartData = False
        self.constraints = constraints
        self.critique = critique
        
    def _mean(self):
        return self.data['int'] + self.data['slope'] * math.log(self.bsa)
        
    def mean(self):
        return math.exp( self._mean() )
    
    def zscore(self):
        try:
            return ( math.log( self.score ) - self._mean() ) / self.data['mse']
        except:
            return None
    
    def lln(self):
        z = self.limit
        return math.exp( self._mean() - (z * self.data['mse']) )

    def uln(self):
        z = self.limit
        return math.exp( self._mean() + (z * self.data['mse']) )

# 
# individual site data
#
#2D
aov = { 'name': 'aov',
       'male': { 'int': 2.78, 'slope': 0.47, 'mse': 0.10 },
       'female': { 'int': 2.75, 'slope': 0.44, 'mse': 0.10 }

}

sov_d = {'name': 'sov_d', 
         'male': { 'int': 3.10, 'slope': 0.49, 'mse': 0.10 }, 
         'female': { 'int': 3.10, 'slope': 0.44, 'mse': 0.09 }
        }

stj_d = { 'name': 'stj_d',
         'male': { 'int': 2.90, 'slope': 0.47, 'mse': 0.10 }, 
         'female': { 'int': 2.90, 'slope': 0.42, 'mse': 0.09 }
}

aao_d = {'name': 'aao_d', 
         'male': { 'int': 2.90, 'slope': 0.46, 'mse': 0.11 }, 
         'female': { 'int': 2.90, 'slope': 0.46, 'mse': 0.10 }
        }


sites = [
    'aov',
    'sov_d',
    'stj_d',
    'aao_d'
]
