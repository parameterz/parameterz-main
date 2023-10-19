#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Mosteller'
name = 'Kaiser et al., JCMR 2008'
description = 'Pediatric Cardiac MRI: BSA-adjusted z-scores for the aortic root and arch.'
keywords = 'cardiac mri z score aortic arch sinus of valsalva isthmus'
citation = {
    'title': '''Normal values for aortic diameters in children and adolescents--
	assessment in vivo by contrast-enhanced CMR-angiography''',
    'authors': 'Kaiser T, Kellenberger CJ, Albisetti M, Bergstrasser E, Valsangiacomo Buechel ER.',
    'journal': 'J Cardiovasc Magn Reson. 2008 Dec 5;10:56.',
    'year': '2008',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/19061495'
}

constraints = {}

class Base(object):
    '''
    This is the base class for the Kaiser/AO model.
        The form of these equations is:
            y = m*x + b
            where x = BSA^0.5
    '''

    def __init__(self, data, pt, limit):
        self.source = name
        self.citation = citation
        self.siteName = data['name']
        self.slope = data['slope']
        self.intercept = data['intercept']
        self.sd = data['sd']
        self.limit = limit
        self.bsaMethod = bsaMethod
        self.bsa = pt.bsa(bsaMethod)
        self.score = float(getattr(pt, data['name']))
        self.constraints = constraints

    def mean(self):
        return self.slope * math.pow(self.bsa, 0.5) + self.intercept

    def zscore(self):
        try:
            return (self.score - self.mean()) / self.sd
        except:
            return None  # property of object 'pt' does not exist

    def uln(self):
        return (self.mean()) + self.limit * self.sd

    def lln(self):
        return (self.mean()) - self.limit * self.sd


# 
# set up the individual sites, using the published data 
# The only difference between 'boys' and 'girls' is the 'a' term...
#
sov = {'name': 'sov', 'slope': 19.37, 'intercept': 0.57, 'sd': 2.38}
stj = {'name': 'stj', 'slope': 16.91, 'intercept': -0.03, 'sd': 1.92}
aao = {'name': 'aao', 'slope': 18.60, 'intercept': -1.33, 'sd': 1.99}
bca = {'name': 'bca', 'slope': 20.07, 'intercept': -3.38, 'sd': 1.69}
t1 = {'name': 't1', 'slope': 18.66, 'intercept': -3.52, 'sd': 1.63}
t2 = {'name': 't2', 'slope': 16.50, 'intercept': -2.63, 'sd': 1.31}
isth = {'name': 'isth', 'slope': 16.52, 'intercept': -3.37, 'sd': 1.46}
dao = {'name': 'dao', 'slope': 14.42, 'intercept': -1.12, 'sd': 1.64}
diaph = {'name': 'diaph', 'slope': 9.89, 'intercept': 1.27, 'sd': 1.34}

sites = [
    'sov',
    'stj',
    'aao',
    'bca',
    't1',
    't2',
    'isth',
    'dao',
    'diaph'
]

inputs = [
    {'id': 'sov',
     'long_name': 'Sinus of Valsalva',
     'title': 'SOV',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'stj',
     'long_name': 'Sino-Tubular Junction',
     'title': 'STJ',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'aao',
     'long_name': 'Ascending Aorta',
     'title': 'AAO',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'bca',
     'long_name': '1st Brachiocephalic Origin',
     'title': 'BCA',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 't1',
     'long_name': 'Proximal Transverse Arch',
     'title': 'PROX TRANS',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 't2',
     'long_name': 'Distal Transverse Arch',
     'title': 'DIST TRANS',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'isth',
     'long_name': 'Isthmus',
     'title': 'ISTH',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'dao',
     'long_name': 'Descending Aorta',
     'title': 'DAO',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'diaph',
     'long_name': 'Aorta at Diaphragm',
     'title': 'DIAPH',
     'units': 'mm',
     'step': '0.1'
     },
]
