#  !/usr/bin/env python

from __future__ import division
from lib import who_bmi


required = ['ht', 'wt', 'age', 'gender']
constraints = {'age': ['12', '17y']}

name = 'Blanchard et al., Med Sci Sports Exerc. 2018'
description = 'Z score equations for several Cardio Respiratory Fitness parameters derived from a healthy pediatric population. '

detail = '''Eighteen cardiorespiratory fitness parameters were analyzed, including VO2 max, RER, max HR, workload, and recovery HR; Z-scores are adjusted for age, gender, and body size.

>"Final prediction models yielded adjusted CRF parameters that were independent of age, sex, body mass, height, body mass index, and Tanner stages."

'''

critique ={
  'model': 'multivariable with height, weight, age, gender',
  'subjects': 228,
  'heterosc': True,
  'residual_assoc': True,
  'residual_heterosc': True,
  'distribution': True,
  'source': 'source article'
}
year = '2018'
citation = {
    'title': 'New Reference Values for Cardiopulmonary Exercise Testing in Children.',
    'authors': 'Blanchard J, Blais S, Chetaille P, Bisson M, Counil FP, Huard-Girard T, Berbari J, Boulay P, Dallaire F.',
    'journal': 'Med Sci Sports Exerc. 2018 Jun;50(6):1125-1133.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/29346167'
}


class Base(object):
    '''
    This is the base class for the Dallaire 'BMI bias' data.
    '''

    def __init__(self, data, pt, limit):
        self.source = name
        self.citation = citation
        self.refName = 'dallaire_pedcard_2015'
        self.siteName = data['name']
        self.ht = float(pt.ht)
        self.wt = float(pt.wt)
        self.age = float(pt.age)
        self.gender = pt.gender
        self.pt = pt
        self.data = data[self.gender]
        self.limit = limit
        self.score = float(getattr(pt, data['name']))
        # chart stuff
        self.chartData = False
        self.constraints = constraints
        self.critique = critique

    def bmiz(self):
        # uses the WHO BMI for Age data
        return who_bmi.getBMIZscore(self.pt)

    def bmi85(self):
        # return the BMI at the 85th percentile according to the WHO data
        return who_bmi.getBMICentile(self.pt, '85')

    def correctedMass(self):
        # returns either the unadjusted pt mass for z < 1.036 or the mass at the BMI 85%ile
        wt = None
        if self.bmiz() <= 1.036:
            wt = self.wt
        else:
            wt = self.bmi85() * (self.ht / 100.0) * (self.ht / 100.0)

        return wt

    def mean(self):
        a = self.data['a']
        b = self.data['b']
        c = self.data['c']
        d = self.data['d']
        e = self.data['e']
        ht = self.ht
        age = self.age
        cMass = self.correctedMass()
        mean = (a * ht * ht) + (b * ht) + (c * cMass) + (d * age) + e
        return mean

    def sd(self):
        # f * ht + g
        return self.data['f'] * self.ht + self.data['g']

    def zscore(self):
        return (self.score - self.mean()) / self.sd()

    def uln(self):
        z = self.limit
        return self.mean() + z * self.sd()

    def lln(self):
        z = self.limit
        return self.mean() - z * self.sd()




#
# individual site data
#


wlmax = {'name': 'wlmax',
          'm': {'a': 0.0182, 'b': -5.324, 'c': 2.824, 'd': 4.170, 'e': 378.9, 'f': 0.220, 'g': -7.62},
          'f': {'a': -0.06025, 'b': 20.57, 'c': 0.741, 'd': 0, 'e': -1622, 'f': 0.284, 'g': -24.41}
         }

wlvt = {'name': 'wlvt',
         'm': {'a': 0.00386, 'b': -0.939, 'c': 1.27, 'd': 0, 'e': 104.4, 'f': 0.251, 'g': -9.28},
         'f': {'a': -0.0122, 'b': 4.09, 'c': 0.601, 'd': 0, 'e': -276.7, 'f': 0.0369, 'g': 17.77}
         }

vo2max = {'name': 'vo2max',
          'm': {'a': -0.297, 'b': 105.90, 'c': 36.6, 'd': 0, 'e': -8660, 'f': 6.45, 'g': -717.1},
          'f': {'a': -0.244, 'b': 86.80, 'c': 14.7, 'd': 0, 'e': -6424, 'f': 2.12, 'g': -45.9}
          }

vo2vt = {'name': 'vo2vt',
          'm': {'a': -0.146, 'b': 56.3, 'c': 18.0, 'd': -48.3, 'e': -3898, 'f': 3.11, 'g': -90.9},
          'f': {'a': -0.00407, 'b': -2.14, 'c': 15.9, 'd': -26.7, 'e': 1282, 'f': 0.454, 'g': 215.3}
          }

pk02pulse = {'name': 'pk02pulse',
         'm': {'a': -0.00131, 'b': 0.459, 'c': 0.214, 'd': 0, 'e': -37.48, 'f': 0.0277, 'g': -2.67},
         'f': {'a': -0.00019, 'b': 0.075, 'c': 0.1007, 'd': 0, 'e': -1.83, 'f': -0.00320, 'g': 2.17}
         }

vemax = {'name': 'vemax',
             'm': {'a': 0.00228, 'b': -0.419, 'c': 0.981, 'd': 3.168, 'e': 2.704, 'f': 0.405, 'g': -52.54},
             'f': {'a': -0.00697, 'b': 2.56, 'c': 0.528, 'd': 1.14, 'e': -202.86, 'f': 0.0681, 'g': 3.72}
             }

pkrer = {'name': 'pkrer',
             'm': {'a': 0, 'b': 0.00142, 'c': -0.000976, 'd': 0.0155, 'e': 0.786, 'f': -0.000161, 'g': 0.0935},
             'f': {'a': 0, 'b': 0.00122, 'c': -0.00195, 'd': 0.0143, 'e': 0.906, 'f': -0.00109, 'g': 0.251}
             }

hrmax = {'name': 'hrmax',
             'm': {'a': -0.000532, 'b': 0.313, 'c': -0.259, 'd': 0, 'e': 169.5, 'f': 0.0966, 'g': -7.47},
             'f': {'a': -0.0213, 'b': 7.198, 'c': -0.193, 'd': -0.809, 'e': -391.1, 'f': -0.121, 'g': 28.41}
             }

oues = {'name': 'oues',
             'm': {'a': -0.171, 'b': 57.8, 'c': 39.1, 'd': 0, 'e': -4247.0, 'f': 8.61, 'g': -1043.0},
             'f': {'a': -0.251, 'b': 91.4, 'c': 13.8, 'd': 0, 'e': -6768.0, 'f': 4.48, 'g': -406.1}
             }

ouesvt = {'name': 'ouesvt',
             'm': {'a': 0.0923, 'b': -30.4, 'c': 32.7, 'd': 0, 'e': 3181.0, 'f': 7.27, 'g': -783.6},
             'f': {'a': -0.0333, 'b': 12.8, 'c': 15.9, 'd': 0, 'e': 35.6, 'f': 5.13, 'g': -476.0}
             }

vevco2sl = {'name': 'vevco2sl',
             'm': {'a': 0, 'b': -0.0407, 'c': 0, 'd': 0, 'e': 35.1, 'f': -0.00559, 'g': 4.48},
             'f': {'a': 0.000191, 'b': -0.112, 'c': 0.0697, 'd': 0, 'e': 37.9, 'f': -0.0103, 'g': 5.37}
             }

vevco2slblwvt = {'name': 'vevco2slblwvt',
             'm': {'a': -0.000918, 'b': 0.319, 'c': -0.0466, 'd': -0.599, 'e': 7.87, 'f': -0.0527, 'g': 11.04},
             'f': {'a': -0.00558, 'b': 1.83, 'c': 0.0191, 'd': -2.901, 'e': -120.7, 'f': 0.00481, 'g': 1.98}
             }

vevco2slatvt = {'name': 'vevco2slatvt',
                 'm': {'a': 0.00128, 'b': -0.434, 'c': -0.0924, 'd': 0, 'e': 68.39, 'f': -0.0289, 'g': 7.28},
                 'f': {'a': -0.00548, 'b': 1.81, 'c': -0.0232, 'd': 0, 'e': -119.1, 'f': 0.0181, 'g': -0.00423}
                 }

o2pulseincr = {'name': 'o2pulseincr',
                 'm': {'a': 0.0139, 'b': -4.03, 'c': -0.534, 'd': 0, 'e': 451.6, 'f': -0.599, 'g': 137.7},
                 'f': {'a': -0.114, 'b': 38.2, 'c': -0.290, 'd': -3.54, 'e': -3002, 'f': 0.509, 'g': -47.4}
                 }

o2pulseslope = {'name': 'o2pulseslope',
                 'm': {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0.0383, 'f': 0, 'g': 0.00748},
                 'f': {'a': 0, 'b': -0.000232, 'c': 0.000108, 'd': 0, 'e': 0.0515, 'f': -0.00000512, 'g': 0.0154}
                 }  # female 'c' term in excel file is 0.000108

vo2slope = {'name': 'vo2slope',
                 'm': {'a': 0, 'b': -0.00871, 'c': 0, 'd': 0, 'e': 12.4, 'f': 0.0121, 'g': -0.995},
                 'f': {'a': 0.00145, 'b': -0.50, 'c': 0.0152, 'd': 0, 'e': 52.17, 'f': -0.00247, 'g': 1.58}
                 }

hrr1 = {'name': 'hrr1',
                 'm': {'a': 0.0168, 'b': -4.91, 'c': -0.439, 'd': 0, 'e': 536.4, 'f': 0.000430, 'g': 12.68},
                 'f': {'a': 0, 'b': 0.225, 'c': -0.0470, 'd': -0.669, 'e': 144.8, 'f': -0.289, 'g': 60.02}
                 }

hrr2 = {'name': 'hrr2',
                 'm': {'a': 0.0168, 'b': 0.627, 'c': -0.556, 'd': -0.679, 'e': 80.17, 'f': 0.0666, 'g': 2.65},
                 'f': {'a': 0, 'b': 0.397, 'c': -0.239, 'd': -0.624, 'e': 110.8, 'f': -0.118, 'g': 32.48}
                 }


sites = [

    'vo2max',
    'wlmax',
    'wlvt',
    'vo2vt',
    'pk02pulse',
    'vemax',
    'pkrer',
    'hrmax',
    'oues',
    'ouesvt',
    'vevco2sl',
    'vevco2slblwvt',
    'vevco2slatvt',
    'o2pulseincr',
    'o2pulseslope',
    'vo2slope',
    'hrr1',
    'hrr2'

]

