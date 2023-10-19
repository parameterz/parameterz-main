#  !/usr/bin/env python

from __future__ import division
import math

required = ['age']
bsaMethod = None
constraints = {'age': [0, 18]}

name = 'Eidem et al., JASE 2004'
description = 'Age-adjusted TDI z-scores.'

detail = '''Age-adjusted reference values and z-scores for tissue Doppler velocities 
according to data published by investigators at Texas Children's Hospital. Pay particular attention to
the units of measure: **cm/sec** (some echo machines default to presenting Doppler measurement data in m/sec).'''
critique ={
  'model': 'linear with Age',
  'subjects': 325,
  'heterosc': False,
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': False,
  'source': 'parameterz'
}
year = '2004'
citation = {
    'title': 'Impact of cardiac growth on Doppler tissue imaging velocities: a study in healthy children.',
    'authors': '''Eidem BW, McMahon CJ, Cohen RR, Wu J, Finkelshteyn I,
    Kovalchin JP, Ayres NA, Bezold LI, O'Brian Smith E, Pignatelli RH.''',
    'journal': 'J Am Soc Echocardiogr. 2004 Mar;17(3):212-21.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/14981417'
}

class Base(object):
    '''
    This is the base class for the Eidem TDI data;
    lookup the nearest age in the ages list and use that index to get mean and
    SD values from the data list
    '''

    def __init__( self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.refName = 'eidem_jase_2004'
        self.siteName = data['name']
        self.limit = limit
        self.score = float(getattr(pt, data['name']))
        self.values = data['values'][getIndex(float(pt.age))]
        #chart stuff
        self.chartData = False
        self.constraints = constraints
        self.critique = critique
        


    def mean(self):
      return self.values[0]
    
    def sd(self, ):
      return self.values[1]

    def zscore(self):
      return (self.score - self.mean()) / self.sd()

    def uln(self):
      return self.mean() + self.limit * self.sd()

    def lln(self):
      return self.mean() - self.limit * self.sd()

def getIndex(target):
  '''return the index of the age, used to lookup data values from the data list'''
  #set upper, lower limits
  if target < 1:
    target = 0.99
  if target > 14:
    target = 14
  # first see if there is an exact match..
  if target in ages:
      return ages.index(target)
  #if not exact match find the age it breaks at
  else:
    for i, j in enumerate(ages):
      if j > target:
          return i -1

# 
# individual site data 
#
ages = [
  #monthly thru 1 year; every year thereafter
  0.99,
  1,
  6,
  10,
  14,
]

rv_tdi_s = { "name": "rv_tdi_s",
         'values': [
          #data are [mean, sd]
          [10.2, 5.5], #<1
          [13.2, 2.0], #1-5y
          [13.4, 2.0], #6-9y
          [13.9, 2.4], #10-13y
          [14.2, 2.3], #14-18y
          ]}

rv_tdi_e = { "name": "rv_tdi_e",
         'values': [
          #data are [mean, sd]
          [13.8, 8.2], #<1
          [17.1, 4.0], #1-5y
          [16.5, 3.0], #6-9y
          [16.5, 3.1], #10-13y
          [16.7, 2.8], #14-18y
          ]}

rv_tdi_a = { "name": "rv_tdi_a",
         'values': [
          #data are [mean, sd]
          [9.8, 2.4], #<1
          [10.9, 2.7], #1-5y
          [9.8, 2.7], #6-9y
          [10.3, 3.4], #10-13y
          [10.1, 2.6], #14-18y
          ]}

septal_tdi_s = { "name": "septal_tdi_s",
         'values': [
          #data are [mean, sd]
          [5.4, 1.2], #<1
          [7.1, 1.5], #1-5y
          [8.0, 1.3], #6-9y
          [8.2, 1.3], #10-13y
          [9.0, 1.5], #14-18y
          ]}

septal_tdi_e = { "name": "septal_tdi_e",
         'values': [
          #data are [mean, sd]
          [8.1, 2.5], #<1
          [11.8, 2.0], #1-5y
          [13.4, 1.9], #6-9y
          [14.5, 2.6], #10-13y
          [14.9, 2.4], #14-18y
          ]}

septal_tdi_a = { "name": "septal_tdi_a",
         'values': [
          #data are [mean, sd]
          [6.1, 1.5], #<1
          [6.0, 1.3], #1-5y
          [5.9, 1.3], #6-9y
          [6.1, 2.3], #10-13y
          [6.2, 1.5], #14-18y
          ]}

lv_tdi_s = { "name": "lv_tdi_s",
         'values': [
          #data are [mean, sd]
          [5.7, 1.6], #<1
          [7.7, 2.1], #1-5y
          [9.5, 2.1], #6-9y
          [10.8, 2.9], #10-13y
          [12.3, 2.9], #14-18y
          ]}

lv_tdi_e = { "name": "lv_tdi_e",
         'values': [
          #data are [mean, sd]
          [9.7, 3.3], #<1
          [15.1, 3.4], #1-5y
          [17.2, 3.7], #6-9y
          [19.6, 3.4], #10-13y
          [20.6, 3.8], #14-18y
          ]}

lv_tdi_a = { "name": "lv_tdi_a",
         'values': [
          #data are [mean, sd]
          [5.7, 1.8], #<1
          [6.5, 1.9], #1-5y
          [6.7, 1.9], #6-9y
          [6.4, 1.8], #10-13y
          [6.7, 1.6], #14-18y
          ]}


sites = [
  'rv_tdi_s',
  'rv_tdi_e',
  'rv_tdi_a',
  'septal_tdi_s',
  'septal_tdi_e',
  'septal_tdi_a',
  'lv_tdi_s',
  'lv_tdi_e',
  'lv_tdi_a'
]
