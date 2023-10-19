#  !/usr/bin/env python

from __future__ import division
import math


required = ['ht', 'wt', 'gender']

constraints = {'age': [0, '18y']}

name = 'Dallaire et al., Ped Card 2015'
description = 'Aortic root z-scores (aortic valve, sinus of Valsalva, and ascending aorta) adjusted for height and weight, specifically designed to minimize bias associated with (increasing) BMI.'

detail = '''Pediatric aortic root z-scores (aortic valve, sinus of Valsalva, and ascending aorta) adjusted for height and weight. 
This multivariable model was developed specifically to minimize z-score bias related to BMI. Particular attention was paid to the statistical design such that resulting z-scores
are valid, without residual association to body size and conforming to a normal distribution with a mean of 0 and an SD of 1.

>"This should be viewed as a proof of concept that bivariate models may be insufficient as a normalization tool
in pediatric echocardiography."
'''

critique ={
  'model': 'multivariable with height and weight',
  'subjects': 1396,
  'heterosc': True,
  'residual_assoc': True,
  'residual_heterosc': True,
  'distribution': True,
  'source': 'source article'
}
year = '2015'
citation = {
    'title': 'Bias Related to Body Mass Index in Pediatric Echocardiographic Z Scores.',
    'authors': 'Dallaire F, Bigras JL, Prsa M, Dahdah N.',
    'journal': 'Pediatr Cardiol. 2015 Mar; 36(3): 667-676.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/25388631'
}

class Base(object):
    '''
    This is the base class for the Dallaire 'BMI bias' data.
    '''

    def __init__( self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.refName = 'dallaire_pedcard_2015'
        self.siteName = data['name']
        self.ht = float(pt.ht)/100
        self.wt = float(pt.wt)
        self.gender = pt.gender
        self.data = data[self.gender]
        self.limit = limit
        self.score = float(getattr(pt, data['name']))
        #chart stuff
        self.chartData = False
        #self.bsaData = [x * 0.1 for x in range(1, 7)] #bsa range is 0.12-0.67
        #self.chartXAxisLabel = 'BSA'
        #self.myData = ( [[self.bsa, self.score]] )#plot data
        self.constraints = constraints
        self.critique = critique


    
    
    def mean(self):
        a = self.data['a']
        b = self.data['b']
        c = self.data['c']
        d = self.data['d']
        e = self.data['e']
        ht = self.ht
        wt = self.wt
        mean = (a * ht * ht) + (b * ht) + (c * math.sqrt(ht)) + (d * math.sqrt(wt)) + e
        return mean
            
        
    
    def sd(self):
        # g * ht + h
        g = self.data['g']
        h = self.data['h']
        return g * self.ht + h
    
    def zscore(self):
        return ( self.score - self.mean() ) / self.sd()

    
    def uln(self):
        z = self.limit
        return self.mean() + z * self.sd()

    
    def lln(self):
        z = self.limit
        return self.mean() - z * self.sd()
        
# 
# individual site data 
# 


aov = { 'name': 'aov', 'm': { 'a': 3.858, 'b': -26.611, 'c': 50.511, 'd': 0.923, 'e': -17.911, 'g': 0.943, 'h': 0.129 },
                       'f': { 'a': 9.164, 'b': -59.845, 'c': 95.358, 'd': 0.754, 'e': -34.544, 'g': 0.665, 'h': 0.359 }
      }
sov = { 'name': 'sov', 'm': { 'a': 3.100, 'b': -15.734, 'c': 40.991, 'd': 0.684, 'e': -13.197, 'g': 1.141, 'h': 0.513 },
                       'f': { 'a': 14.478, 'b': -83.380, 'c': 127.421, 'd': 0.637, 'e': -43.906, 'g': 1.316, 'h': 0.172 }
      }
aao = { 'name': 'aao', 'm': { 'a': -10.202, 'b': 74.192, 'c': -86.798, 'd': 0.717, 'e': 35.442, 'g': 0.836, 'h': 0.707 },
                       'f': { 'a': 9.160, 'b': -44.664, 'c': 69.321, 'd': 0.653, 'e': -21.262, 'g': 0.958, 'h': 0.354 } #these last values for calculating sd seems wrong; updated via personal communication; errata pending
      }

sites = [
    
    'aov',
    'sov',
    'aao'
    
]
