#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Mosteller'

name = 'Knobel et al., IJCI 2011'
description = 'Pediatric Cardiac MRI: BSA-adjusted z-scores for the MPA, RPA, and LPA.'
keywords = 'cardiac mri z score MPA RPA LPA Pulmonary Artery'
citation = {
    'title': '''Geometry and dimensions of the pulmonary artery bifurcation
	in children and adolescents: assessment in vivo by contrast-enhanced
	MR-angiography ''',
    'authors': 'Knobel Z, Kellenberger CJ, Kaiser T, Albisetti M, Bergstrasser E, Buechel ER.',
    'journal': 'Int J Cardiovasc Imaging. 2011 Mar;27(3):385-96.',
    'year': '2011',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/20652636'
}
constraints = {}

class Base(object):
    '''
    This is the base class for the Knobel/PA model.
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
# individual site data 
#

mpa_axial = {'name': 'mpa_axial', 'slope': 13.43, 'intercept': 4.85, 'sd': 2.72}
mpa_sagittal = {'name': 'mpa_sagittal', 'slope': 17.07, 'intercept': 1.04, 'sd': 2.01}
rpa_prox_axial = {'name': 'rpa_prox_axial', 'slope': 9.19, 'intercept': 2.63, 'sd': 1.65}
rpa_dist_axial = {'name': 'rpa_dist_axial', 'slope': 6.25, 'intercept': 3.9, 'sd': 1.49}
rpa_prox_rao = {'name': 'rpa_prox_rao', 'slope': 14.3, 'intercept': -0.69, 'sd': 1.76}
rpa_dist_rao = {'name': 'rpa_dist_rao', 'slope': 14.62, 'intercept': -1.08, 'sd': 1.6}
lpa_prox_axial = {'name': 'lpa_prox_axial', 'slope': 11.27, 'intercept': 1.7, 'sd': 1.37}
lpa_dist_axial = {'name': 'lpa_dist_axial', 'slope': 11.89, 'intercept': -0.1, 'sd': 1.51}
lpa_prox_lao = {'name': 'lpa_prox_lao', 'slope': 16.82, 'intercept': -2.13, 'sd': 1.88}
lpa_dist_lao = {'name': 'lpa_dist_lao', 'slope': 13.64, 'intercept': -2.08, 'sd': 1.5}

sites = [
    'mpa_axial',
    'mpa_sagittal',
    'rpa_prox_axial',
    'rpa_dist_axial',
    'rpa_prox_rao',
    'rpa_dist_rao',
    'lpa_prox_axial',
    'lpa_dist_axial',
    'lpa_prox_lao',
    'lpa_dist_lao'
]

inputs = [
    {'id': 'mpa_axial',
     'long_name': 'MPA, Axial',
     'title': 'MPA AX',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'mpa_sagittal',
     'long_name': 'MPA, Sagittal',
     'title': 'MPA SAG',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'rpa_prox_axial',
     'long_name': 'RPA, Proximal, Axial',
     'title': 'RPA PROX AX',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'rpa_dist_axial',
     'long_name': 'RPA, Distal, Axial',
     'title': 'RPA DIST AX',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'rpa_prox_rao',
     'long_name': 'RPA, Proximal, RAO',
     'title': 'RPA PROX RAO',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'rpa_dist_rao',
     'long_name': 'RPA, Distal, RAO',
     'title': 'RPA DIST RAO',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'lpa_prox_axial',
     'long_name': 'LPA, Proximal, Axial',
     'title': 'LPA PROX AX',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'lpa_dist_axial',
     'long_name': 'LPA, Distal, Axial',
     'title': 'LPA DIST AX',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'lpa_prox_lao',
     'long_name': 'LPA, Proximal, LAO',
     'title': 'LPA PROX LAO',
     'units': 'mm',
     'step': '0.1'
     },
    {'id': 'lpa_dist_lao',
     'long_name': 'LPA, Distal, LAO',
     'title': 'LPA DIST LAO',
     'units': 'mm',
     'step': '0.1'
     },
]
