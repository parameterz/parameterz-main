#!/usr/bin/env python
'''
This one is a *bit* of an experiment.
The authors used a validation cohort (N=122) to test their model; the validation cohorts'
RMSE values are used to generate confidence intervals (which are used here
as SD values).
'''
from __future__ import division
import math

required = ['wt', 'ht', 'gender', 'age']
bsaMethod = None
name = 'Pfaffenberger et al., Circ CV Img 2013'
year = '2006'
description = 'Size, age, and gender adjusted reference values for adult echocardiography measurements.'

detail ='''Multivariable linear regression analyses of the impact of sex, age,
height, and weight on cardiac chamber size. Data is from the echo lab at the
Medical University in Vienna, Austria.
>The present work shows that sex, age, and body size affect the normal heart
>size. These parameters need to be considered when cutoff values indicating
>the need for treatment or even surgery are applied.
'''
critique = {
  'model': 'multiple linear regression with height, weight, age, and gender',
  'subjects': 622,
  'heterosc': False,
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': False,
  'source': 'parameterz'
}
citation = {
    'title': 'Size matters! Impact of age, sex, height, and weight on the normal heart size.',
    'authors': 'Pfaffenberger S, Bartko P, Graf A, Pernicka E, Babayev J, Lolic E, Bonderman D, Baumgartner H, Maurer G, Mascherbauer J.',
    'journal': 'Circ Cardiovasc Imaging. 2013 Nov;6(6):1073-9.',
    'year': '2013',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/24014823'
}
constraints = {'age': [17, 91], 'ht': [143, 200], 'wt': [32, 240]}

class Base(object):
    '''Base class for Pfaffenberger z-scores'''
    def __init__(self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.siteName = data['name']
        self.refName = 'pfaffenberger_circimaging_2013'
        self.wt = float(pt.wt)
        self.ht = float(pt.ht)
        self.gender = 1 if pt.gender == 'f' else 0
        self.age = float(pt.age)
        self.score = float(getattr(pt, data['name']))
        self.int = data['int']
        self.w = data['w']
        self.h = data['h']
        self.g = data['g']
        self.a = data['a']
        self.rmse = data['rmse']
        self.limit = limit
        #chart stuff
        self.chartData = False
        self.constraints = constraints
        self.critique = critique
        
    def mean(self):
        return self.int + (self.ht * self.h) + (self.wt * self.w) + (self.age * self.a) + (self.gender * self.g)
    
    def zscore(self):
        return ( self.score - self.mean() ) / self.rmse
    
    def lln(self):
        z = self.limit
        return self.mean() - (z * self.rmse)

    def uln(self):
        z = self.limit
        return self.mean() + (z * self.rmse)

# 
# individual site data
#
#2D
lv_minor = {'name': 'lv_minor', 'int': 20.98637, 'w': 0.07404, 'h': 0.11429, 'g': -1.45756, 'a': -0.04141, 'rmse': 3.21}
lvedv = {'name': 'lvedv', 'int': -39.37731, 'w': 0.42808, 'h': 0.73703, 'g': -9.47838, 'a': -0.33895, 'rmse': 18.73}
rv_minor = {'name': 'rv_minor', 'int': 15.94580, 'w': 0.04375, 'h': 0.07014, 'g': -2.35620, 'a': 0, 'rmse': 3.38}
rv_area = {'name': 'rv_area', 'int': -0.97314, 'w': 0.09270, 'h': 0.10040, 'g': -2.62433, 'a': -0.03906, 'rmse': 4.42}
la = {'name': 'la', 'int': 34.23014, 'w': 0.11356, 'h': 0, 'g': -1.73000, 'a': 0.09453, 'rmse': 3.93} #2D LA Diam?
la_area = {'name': 'la_area', 'int': -4.07280, 'w': 0.05673, 'h': 0.08135, 'g': 0, 'a': 0.02779, 'rmse': 2.70}
lav = {'name': 'lav', 'int': -34.73810, 'w': 0.21533, 'h': 0.31554, 'g': 0, 'a': 0.10538, 'rmse': 11.84}
ra = {'name': 'ra', 'int': 35.52012, 'w': 0.10712, 'h': 0, 'g': -2.03817, 'a': 0.08743, 'rmse': 3.55} 
ra_area = {'name': 'ra_area', 'int': 9.15398, 'w': 0.7818, 'h': 0, 'g': -1.85918, 'a': 0, 'rmse': 2.37}
rav = {'name': 'rav', 'int': 18.97912, 'w': 0.27999, 'h': 0, 'g': -8.55635, 'a': 0, 'rmse': 10.35}
#mmodes
lvedd_mm = {'name': 'lvedd_mm', 'int': 15.38196, 'w': 0.07658, 'h': 0.15007, 'g': 0, 'a': 0, 'rmse': 3.66}
lvesd_mm = {'name': 'lvesd_mm', 'int': 26.76878, 'w': 0.04765, 'h': 0, 'g': -2.11032, 'a': 0, 'rmse': 0}#article is missing rmse for this...
ivsd_mm = {'name': 'ivsd_mm', 'int': 7.34011, 'w': 0.01872, 'h': 0, 'g': -0.53678, 'a': 0.02469, 'rmse': 0.90}
lvpwd_mm = {'name': 'lvpwd_mm', 'int': 7.49088, 'w': 0.01964, 'h': 0, 'g': -0.57818, 'a': 0.01489, 'rmse': 0.91}

sites = [
    'ivsd_mm',
    'lvedd_mm',
    'lvpwd_mm',
    #'lvesd_mm', #missing rmse = no z-score
    'lv_minor',
    'lvedv',
    'rv_minor',
    'rv_area',
    'la',
    'la_area',
    'lav',
    'ra',
    'ra_area',
    'rav'
]
