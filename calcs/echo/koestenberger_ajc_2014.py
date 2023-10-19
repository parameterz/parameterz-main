#  !/usr/bin/env python

from __future__ import division
import math


required = ['age', 'gender']

constraints = {'age': [0, '18y']}

name = 'Koestenberger et al., Am J Cardiol 2014'
description = 'z-scores of the right ventricle (RV) diameters and areas'

detail = '''Age-adjusted z-scores of the right ventricle (RV) diameters and areas, as measured from the apical four-chamber view.

>Quantitative assessments of dilated RV dimensions using 2D echocardiography in children cannot be done without first having age-related normative data.
'''

critique ={
  'model': 'mostly nonlinear realtionships with age',
  'subjects': 576,
  'heterosc': True,
  'residual_assoc': True,
  'residual_heterosc': True,
  'distribution': True,
  'source': 'source article'
}
year = '2014'
citation = {
    'title': 'Reference values and calculation of z-scores of echocardiographic measurements of the normal pediatric right ventricle.',
    'authors': 'Koestenberger M, Nagel B, Ravekes W, Avian A, Burmas A, Grangl G, Cvirn G, Gamillscheg A.',
    'journal': 'Am J Cardiol. 2014 Nov 15;114(10):1590-8.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/25248810'
}

class Base(object):
    '''
    This is the base class for the Koestenberger RV data.
    '''

    def __init__( self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.refName = 'koestenberger_ajc_2014'
        self.siteName = data['name']
        self.age = float(pt.age)
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


    def _mean(self):
        #a+b*age^0.5
        return self.data["a"] + self.data["b"] * math.pow( self.age, 0.5)
    
    def mean(self):
        if self.data["eqnType"] == "linear":
            #a+b*age^0.5
            return 10 * ( self.data["a"] + self.data["b"] * math.pow( self.age, 0.5) )
        
        if self.data["eqnType"] == "log-linear":
            mean =  math.exp( self._mean() )
            return mean if self.siteName in ['rv_eda_a4c', 'rv_esa_a4c'] else 10 * mean
        
        if self.data["eqnType"] == "quadratic":
            mean = math.pow( self._mean(), 2 )
            return mean if self.siteName in ['rv_eda_a4c', 'rv_esa_a4c'] else 10 * mean
    
    def sd(self):
        #these are ALL linear in the form c+d*age^0.5
        sd1 = self.data["c"] - self.data["d"] * math.pow( self.age, 0.5)
        sd2 = self.data["c"] + self.data["d"] * math.pow( self.age, 0.5)
        return sd2 if self.siteName in ['rv_len', 'rv_eda_a4c'] else sd1
    
    def zscore(self):
        score = self.score if self.siteName in ['rv_eda_a4c', 'rv_esa_a4c'] else self.score / 10
        if self.data["eqnType"] == "linear":
            return ( score - self._mean() ) / self.sd()

        if self.data["eqnType"] == "quadratic":
            return ( math.pow( score, 0.5 ) - self._mean() ) / self.sd()

        if self.data["eqnType"] == "log-linear":
            return ( math.log( score ) - self._mean() ) / self.sd()
        
        
    def uln(self):
        z = self.limit
        if self.data["eqnType"] == "linear":
            return 10 * ( self._mean() + z * self.sd() )

        if self.data["eqnType"] == "log-linear":
            uln =  math.exp( self._mean() + z * self.sd() )
            return uln if self.siteName in ['rv_eda_a4c', 'rv_esa_a4c'] else uln * 10

        if self.data["eqnType"] == "quadratic":
            uln = math.pow( self._mean() + z * self.sd(), 2)
            return uln if self.siteName in ['rv_eda_a4c', 'rv_esa_a4c'] else uln * 10


    def lln(self):
        z = self.limit
        if self.data["eqnType"] == "linear":
            return 10 * ( self._mean() - z * self.sd() )

        if self.data["eqnType"] == "log-linear":
            lln = math.exp( self._mean() - z * self.sd() )
            return lln if self.siteName in ['rv_eda_a4c', 'rv_esa_a4c'] else lln * 10

        if self.data["eqnType"] == "quadratic":
            lln = math.pow( self._mean() - z * self.sd(), 2)
            return lln if self.siteName in ['rv_eda_a4c', 'rv_esa_a4c'] else lln * 10

# 
# individual site data 
# 


#only these are gender-specific
rv_len_es = { "name": "rv_len_es",
            "m": {"eqnType": "log-linear", "a": 0.51, "b": 0.28, "c": 0.171, "d": 0.007 },
            "f": {"eqnType": "log-linear", "a": 0.50, "b": 0.27, "c": 0.160, "d": 0.002 }
        }

#all the rest are the same values for m and f
#but for the sake of simplicity of the base class I built the objects as tho they are all gender specific
rv_len = { "name": "rv_len",
            "m": {"eqnType": "linear", "a": 2.03, "b": 1.10, "c": 0.510, "d": 0.042 },
            "f": {"eqnType": "linear", "a": 2.03, "b": 1.10, "c": 0.510, "d": 0.042 }
        }

rv_b_a4c = { "name": "rv_b_a4c",
            "m": { "eqnType": "log-linear", "a": 0.28, "b": 0.25, "c": 0.174, "d": 0.005 },
            "f":  { "eqnType": "log-linear", "a": 0.28, "b": 0.25, "c": 0.174, "d": 0.005 }
        }

rv_mc_a4c = { "name": "rv_mc_a4c",
            "m": { "eqnType":"log-linear", "a": 0.15, "b": 0.25, "c": 0.180, "d": 0.006 },
            "f": { "eqnType":"log-linear", "a": 0.15, "b": 0.25, "c": 0.180, "d": 0.006 }
        }

rv_eda_a4c = { "name": "rv_eda_a4c",
            "m": { "eqnType": "quadratic", "a": 1.47, "b": 0.70, "c": 0.295, "d": 0.019 },
            "f": { "eqnType": "quadratic", "a": 1.47, "b": 0.70, "c": 0.295, "d": 0.019 }
        }

rv_esa_a4c = { "name": "rv_esa_a4c",
            "m": { "eqnType": "log-linear", "a": 0.42, "b": 0.50, "c": 0.310, "d": 0.014 },
            "f": { "eqnType": "log-linear", "a": 0.42, "b": 0.50, "c": 0.310, "d": 0.014 }
        }


sites = [
    
    'rv_len',
    'rv_len_es',
    'rv_b_a4c',
    'rv_mc_a4c',
    'rv_eda_a4c',
    'rv_esa_a4c'    
]
