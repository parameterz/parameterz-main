#  !/usr/bin/env python

from __future__ import division
import math

required = ['wt', 'age']
bsaMethod = None
constraints = {'age': [0, '2d']}

name = 'Jain et al., JASE 2014'
description = 'Weight-adjusted z-scores of the right ventricular for newborns: Tricuspid valve z-score, RV strain z-score, RV diameter z-score, tissue Doppler z-score, TAPSE z-score'

detail = '''Z-scores of the right heart for newborns (1-2 days). Reference values for the tricuspid annulus, RV chamber diameters, RV areas; also z-scores of RV systolic and diastolic function parameters.'''

critique ={
  'model': 'linear models with weight',
  'subjects': 50,
  'heterosc': True,
  'residual_assoc': True,
  'residual_heterosc': True,
  'distribution': True,
  'source': 'parameterz'
}
year = '2014'
citation = {
    'title': '''A Comprehensive Echocardiographic Protocol for Assessing Neonatal Right Ventricular Dimensions and Function in the Transitional Period: Normative Data and Z Scores.''',
    'authors': '''Jain A, Mohamed A, El-Khuffash A, Connelly KA, Dallaire F, Jankov RP, McNamara PJ, Mertens L.''',
    'journal': 'J Am Soc Echocardiogr. 2014 Dec;27(12):1293-304.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/25260435'
}

class Base(object):
    '''
    This is the base class for the Jain data.
    There are several forms of these equations, and some of them are age dependent.
    Most of the equations are linear with wt.
    ONE of the equations (S'/D' ratio) is a log transformation, but I don't think I am going to bother to calculate this...
    Other data are not related to wt and thus are just mean and sd data
    '''

    def __init__( self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.refName = 'jain_jase_2014'
        self.siteName = data['name']
        self.wt = float(pt.wt)
        self.age = float(pt.age)
        self.eqnType = data['eqnType']
        self.measType = data['measType']
        self.values = data['d2'] if self.age > 0.005 else data['d1'] #0.005 is almost 2 days old as a decimal
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
        return (self.values['intercept'] + self.values['slope'] * self.wt) 
    
    def _mean2(self):
        #returns the untransformed mean value (no equation)
        return self.values['mean']
    
    def mean(self):
        if self.eqnType == 'linear' and self.measType == 'linear': #convert from cm to mm
            return 10 * self._mean()
        if self.eqnType == 'linear' and self.measType in ['area', 'pct']: #do not convert
            return self._mean()
        if self.eqnType == 'none' and self.measType in ['doppler', 'strain']: #do not convert
            return self.values['mean']
        if self.eqnType == 'none' and self.measType == 'linear': #convert from cm to mm
            return 10 * self._mean2()
    
    def zscore(self):
        if self.eqnType == 'linear' and self.measType == 'linear': #convert from cm to mm
            return ( self.score/10 - self._mean()) / self.values['sd'] 
        if self.eqnType == 'linear' and self.measType in ['area', 'pct']: #do not convert
            return ( self.score - self._mean()) / self.values['sd'] 
        if self.eqnType == 'none' and self.measType in ['doppler', 'strain']: #do not convert
            return ( self.score - self.values['mean'] ) / self.values['sd']
        if self.eqnType == 'none' and self.measType == 'linear': #convert from cm to mm
            return ( self.score/10 - self._mean2()) / self.values['sd'] 
    
    def uln(self):
        z = self.limit
        if self.eqnType == 'linear' and self.measType == 'linear': #convert from cm to mm
            return 10 * (self._mean() + z * self.values['sd']) 
        if self.eqnType == 'linear' and self.measType in ['area', 'pct']: #do not convert
            return (self._mean() + z * self.values['sd'])     
        if self.eqnType == 'none' and self.measType in ['doppler', 'strain']: #do not convert
            return (self.mean() + z * self.values['sd'])
        if self.eqnType == 'none' and self.measType == 'linear': #convert from cm to mm
            return 10 * (self._mean2() + z * self.values['sd']) 
    
    def lln(self):
        z = self.limit
        if self.eqnType == 'linear' and self.measType == 'linear': #convert from cm to mm
            return 10 * (self._mean() - z * self.values['sd']) 
        if self.eqnType == 'linear' and self.measType in ['area', 'pct']: #do not convert units
            return (self._mean() - z * self.values['sd']) 
        if self.eqnType == 'none' and self.measType in ['doppler', 'strain']: #do not convert
            return (self.mean() - z * self.values['sd'])
        if self.eqnType == 'none' and self.measType == 'linear': #convert from cm to mm
            return 10 * (self._mean2() - z * self.values['sd']) 
        
# 
# individual site data 
# d2 is the same as d1 in many cases... and while it makes the individual dicts slightly bigger,
# it makes for a more uniform appearance and a straightforward d1/d2 calculation
#

tvd_l = { "name": "tvd_l", "eqnType": "linear", "measType": "linear",  
         "d1": { "intercept": 1.14, "slope": 0.044, "sd": 0.151 },
         "d2": { "intercept": 1.14, "slope": 0.044, "sd": 0.151 }
        }

rv_b_a4c = { "name": "rv_b_a4c", "eqnType": "linear", "measType": "linear", 
         "d1": { "intercept": 1.20, "slope": 0.146, "sd": 0.158 },
         "d2": { "intercept": 1.20, "slope": 0.146, "sd": 0.158 }
        }

rv_mc_a4c = { "name": "rv_mc_a4c", "eqnType": "linear", "measType": "linear", 
         "d1": { "intercept": 0.86, "slope": 0.197, "sd": 0.169 },
         "d2": { "intercept": 1.12, "slope": 0.168, "sd": 0.183 }
        }

rv_len = { "name": "rv_len", "eqnType": "linear", "measType": "linear", 
          "d1": { "intercept": 2.52, "slope": 0.154, "sd": 0.219 },
          "d2": { "intercept": 2.52, "slope": 0.154, "sd": 0.219 }
        }

rv_b_plax = { "name": "rv_b_plax", "eqnType": "linear", "measType": "linear", 
          "d1": { "intercept": 1.89, "slope": 0.048, "sd": 0.243 },
          "d2": { "intercept": 1.70, "slope": 0.153, "sd": 0.279 }
        }

rv_eda_a4c = { "name": "rv_eda_a4c", "eqnType": "linear", "measType": "area", 
         "d1": { "intercept": 1.16, "slope": 0.841, "sd": 0.581 },
         "d2": { "intercept": 1.16, "slope": 0.841, "sd": 0.581 } 
        }

rv_esa_a4c = { "name": "rv_esa_a4c", "eqnType": "linear", "measType": "area", 
         "d1": { "intercept": -0.11, "slope": 0.893, "sd": 0.418 },
         "d2": { "intercept": -0.11, "slope": 0.893, "sd": 0.418 } 
        }

rv_fac_a4c = { "name": "rv_fac_a4c", "eqnType": "linear", "measType": "pct", 
         "d1": { "intercept": 48.0, "slope": -6.30, "sd": 6.67 }, #values are 100* the published values in order to show as a percent (rather than decimal)
         "d2": { "intercept": 48.0, "slope": -6.30, "sd": 6.67 }
        }

rv_eda_3c = { "name": "rv_eda_3c", "eqnType": "linear", "measType": "area", 
         "d1": { "intercept": 1.62, "slope": 1.373, "sd": 1.014 },
         "d2": { "intercept": 1.62, "slope": 1.373, "sd": 1.014 } 
        }

rv_esa_3c = { "name": "rv_esa_3c", "eqnType": "linear", "measType": "area", 
         "d1": { "intercept": 1.58, "slope": 0.667, "sd": 0.607 },
         "d2": { "intercept": 1.58, "slope": 0.667, "sd": 0.607 } 
        }

rv_fac_3c = { "name": "rv_fac_3c", "eqnType": "linear", "measType": "pct", 
         "d1": { "intercept": 30.0, "slope": 2.5, "sd": 6.70 }, #values are 100* the published values in order to show as a percent (rather than decimal)
         "d2": { "intercept": 30.0, "slope": 2.5, "sd": 6.70 }
        }

rv_fac_global = { "name": "rv_fac_global", "eqnType": "linear", "measType": "pct", 
         "d1": { "intercept": 40.0, "slope": -2.1, "sd": 5.20 }, #values are 100* the published values in order to show as a percent (rather than decimal)
         "d2": { "intercept": 40.0, "slope": -2.1, "sd": 5.20 }
        }

tapse = { "name": "tapse", "eqnType": "none", "measType": "linear", 
        "d1": { "mean": 0.92, "sd": 0.14 },
        "d2": { "mean": 0.92, "sd": 0.14 }
        }

rv_tdi_e = { "name": "rv_tdi_e", "eqnType": "none", "measType": "doppler", 
        "d1": { "mean": 7.9954, "sd": 1.5731 },
        "d2": { "mean": 7.9954, "sd": 1.5731 }
        }

rv_tdi_a = { "name": "rv_tdi_a", "eqnType": "none", "measType": "doppler", 
        "d1": { "mean": 8.2676, "sd": 1.5731 },
        "d2": { "mean": 8.2676, "sd": 1.5731 }
        }

rv_tdi_s = { "name": "rv_tdi_s", "eqnType": "none", "measType": "doppler", 
        "d1": { "mean": 6.5534, "sd": 1.1587 },
        "d2": { "mean": 6.5534, "sd": 1.1587 }
        }

rv_pls_a4c = { "name": "rv_pls_a4c", "eqnType": "none", "measType": "strain", 
        "d1": { "mean": 21.17, "sd": 5.25 },
        "d2": { "mean": 21.17, "sd": 5.25 }
        }

rv_pls_3c = { "name": "rv_pls_3c", "eqnType": "none", "measType": "strain", 
        "d1": { "mean": 21.38, "sd": 4.36 },
        "d2": { "mean": 21.38, "sd": 4.36 }
        }

rv_pls_global = { "name": "rv_pls_global", "eqnType": "none", "measType": "strain", 
        "d1": { "mean": 21.21, "sd": 3.93 },
        "d2": { "mean": 21.21, "sd": 3.93 }
        }

tv_e = { "name": "tv_e", "eqnType": "none", "measType": "doppler", 
        "d1": { "mean": 45.6, "sd": 9.48 },
        "d2": { "mean": 45.6, "sd": 9.48 }
        }

tv_a = { "name": "tv_a", "eqnType": "none", "measType": "doppler", 
        "d1": { "mean": 52.09, "sd": 10.49 },
        "d2": { "mean": 52.09, "sd": 10.49 }
        }

tv_ea_ratio = { "name": "tv_ea_ratio", "eqnType": "none", "measType": "doppler", 
        "d1": { "mean": 0.89, "sd": 0.17 },
        "d2": { "mean": 0.89, "sd": 0.17 }
        }

rv_tdi_ea_ratio = { "name": "rv_tdi_ea_ratio", "eqnType": "none", "measType": "doppler", 
        "d1": { "mean": 0.99, "sd": 0.23 },
        "d2": { "mean": 0.99, "sd": 0.23 }
        }

tv_Ee_ratio = { "name": "tv_Ee_ratio", "eqnType": "none", "measType": "doppler", 
        "d1": { "mean": 5.85, "sd": 1.34 },
        "d2": { "mean": 5.85, "sd": 1.34 }
        }



sites = [
    
    'tvd_l',
    'rv_b_a4c',
    'rv_mc_a4c',
    'rv_len',
    'rv_b_plax',
    'rv_eda_a4c',
    'rv_esa_a4c',
    'rv_fac_a4c',
    'rv_eda_3c',
    'rv_esa_3c',
    'rv_fac_3c',
    'rv_fac_global',
    'tapse',
    'tv_e',
    'tv_a',
    'tv_ea_ratio',
    'rv_tdi_e',
    'rv_tdi_a',
    'rv_tdi_ea_ratio',
    'rv_tdi_s',
    'rv_pls_a4c',
    'rv_pls_3c',
    'rv_pls_global',
    'tv_Ee_ratio'
    
]
