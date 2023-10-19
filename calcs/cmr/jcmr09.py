#!/usr/bin/env python

from __future__ import division
import math
import config

required = ['bsa', 'gender']
bsaMethod = 'Mosteller'
name = 'Beuchel et al., JCMR 2009'
description = 'Pediatric Cardiac MRI: BSA adjusted z-scores for ventricular volume and mass.'
keywords = 'cardiac mri z score LV Volume LVEDV LV Mass RV Volume RVEDV'
citation = {
    'title': '''Normal right- and left ventricular volumes and myocardial
		mass in children measured by steady state free precession
		cardiovascular magnetic resonance.''',
    'authors': 'Buechel EV, Kaiser T, Jackson C, Schmitz A, Kellenberger CJ',
    'journal': 'J Cardiovasc Magn Reson. 2009 Jun 21;11:19.',
    'year': '2009',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/19545393'
}

constraints = {}

class Base(object):
    ''' This is the base class for the Zurich model.
        The form of these equations is:
            y = aX^b
            where X = BSA'''

    def __init__(self, data, pt, limit):
        self.source = name
        self.citation = citation
        self.siteName = data['name']
        self.boys = data['boys']
        self.girls = data['girls']
        self.limit = limit
        self.bsaMethod = bsaMethod
        self.bsa = pt.bsa(bsaMethod)
        self.score = float(getattr(pt, data['name']))
        self.gender = getattr(pt, 'gender')
        self.constraints = constraints

    def _getGender(self):
        if self.gender == 'm':
            return self.boys
        else:
            return self.girls

    def mean(self):
        gender = self._getGender()
        return gender['a'] * math.pow(self.bsa, gender['b'])

    def zscore(self):
        gender = self._getGender()
        try:
            z = math.log10(self.score / self.mean()) / gender['sd']
            return z
        except:
            return None  # property of object 'pt' does not exist

    def uln(self):
        gender = self._getGender()
        uln = math.log10(self.mean()) + self.limit * gender['sd']
        return math.pow(10, uln)

    def lln(self):
        gender = self._getGender()
        lln = math.log10(self.mean()) - self.limit * gender['sd']
        return math.pow(10, lln)


#
# set up the individual site data.
# The only difference between 'boys' and 'girls' is the 'a' term...
#

lvedv = {
    'name': 'lvedv',
    'boys': {'a': 77.5, 'b': 1.380, 'sd': 0.0426},
    'girls': {'a': 67.8, 'b': 1.380, 'sd': 0.0426}
}

lvesv = {
    'name': 'lvesv',
    'boys': {'a': 29.7, 'b': 1.370, 'sd': 0.0647},
    'girls': {'a': 26.1, 'b': 1.370, 'sd': 0.0647}
}

lvsv = {
    'name': 'lvsv',
    'boys': {'a': 47.4, 'b': 1.394, 'sd': 0.0500},
    'girls': {'a': 41.7, 'b': 1.394, 'sd': 0.0500}
}

lvco = {
    'name': 'lvco',
    'boys': {'a': 3890, 'b': 1.062, 'sd': 0.0727},
    'girls': {'a': 3622, 'b': 1.062, 'sd': 0.0727}
}

lvm = {
    'name': 'lvm',
    'boys': {'a': 53, 'b': 1.304, 'sd': 0.0475},
    'girls': {'a': 45.2, 'b': 1.304, 'sd': 0.0475}
}

paps = {
    'name': 'paps',
    'boys': {'a': 1.9, 'b': 1.451, 'sd': 0.0976},
    'girls': {'a': 1.6, 'b': 1.451, 'sd': 0.0976}
}

rvedv = {
    'name': 'rvedv',
    'boys': {'a': 83.8, 'b': 1.469, 'sd': 0.0499},
    'girls': {'a': 72.7, 'b': 1.469, 'sd': 0.0499}
}

rvesv = {
    'name': 'rvesv',
    'boys': {'a': 35.3, 'b': 1.559, 'sd': 0.0737},
    'girls': {'a': 30.2, 'b': 1.559, 'sd': 0.0737}
}

rvsv = {
    'name': 'rvsv',
    'boys': {'a': 48.2, 'b': 1.407, 'sd': 0.0524},
    'girls': {'a': 42.1, 'b': 1.407, 'sd': 0.0524}
}

rvco = {
    'name': 'rvco',
    'boys': {'a': 3947, 'b': 1.076, 'sd': 0.0783},
    'girls': {'a': 3658, 'b': 1.076, 'sd': 0.0783}
}

rvm = {
    'name': 'rvm',
    'boys': {'a': 16.7, 'b': 1.331, 'sd': 0.0605},
    'girls': {'a': 14.9, 'b': 1.331, 'sd': 0.0605}
}

sites = [
    'lvedv',
    'lvesv',
    'lvsv',
    'lvco',
    'lvm',
    'paps',
    'rvedv',
    'rvesv',
    'rvsv',
    'rvco',
    'rvm'
]

inputs = [
    {'id': 'lvedv',
     'long_name': 'LV End Diastolic Volume',
     'title': 'LVEDV',
     'units': 'ml',
     'step': '0.1'
     },
    {'id': 'lvesv',
     'long_name': 'LV End Systolic Volume',
     'title': 'LVESV',
     'units': 'ml',
     'step': '0.1'
     },
    {'id': 'lvsv',
     'long_name': 'LV Stroke Volume',
     'title': 'LVSV',
     'units': 'ml',
     'step': '0.1'
     },
    {'id': 'lvco',
     'long_name': 'LV Cardiac Output',
     'title': 'LVCO',
     'units': 'ml/min',
     'step': '1'
     },
    {'id': 'lvm',
     'long_name': 'LV Mass',
     'title': 'LVM',
     'units': 'g',
     'step': '0.1'
     },
    {'id': 'paps',
     'long_name': 'Papillary Muscles',
     'title': 'PAP MUSC',
     'units': 'g',
     'step': '0.1'
     },
    {'id': 'rvedv',
     'long_name': 'RV End Diastolic Volume',
     'title': 'RVEDV',
     'units': 'ml',
     'step': '0.1'
     },
    {'id': 'rvesv',
     'long_name': 'RV End Systolic Volume',
     'title': 'RVESV',
     'units': 'ml',
     'step': '0.1'
     },
    {'id': 'rvsv',
     'long_name': 'RV Stroke Volume',
     'title': 'RVSV',
     'units': 'ml',
     'step': '0.1'
     },
    {'id': 'rvco',
     'long_name': 'RV Cardiac Output',
     'title': 'RVCO',
     'units': 'ml/min',
     'step': '1'
     },
    {'id': 'rvm',
     'long_name': 'RV Mass',
     'title': 'RVM',
     'units': 'g',
     'step': '0.1'
     },
]
