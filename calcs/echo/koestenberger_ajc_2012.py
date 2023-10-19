#  !/usr/bin/env python

from __future__ import division
import math

required = ['age']
bsaMethod = None
constraints = {'age': [0, 18]}

name = 'Koestenberger et al., Am J Cardiol 2012'
description = 'Age-adjusted RV systolic function z-scores using tissue Doppler.'

detail = '''Age-adjusted z-scores of RV systolic function using
_tricuspid annular peak systolic velocity_ (TAPSV), perhaps better known as RV TDI s'.
'''
critique ={
  'model': 'nonlinear with Age',
  'subjects': 860,
  'heterosc': False,
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': False,
  'source': 'parameterz'
}
year = '2012'
citation = {
    'title': '''Reference values of tricuspid annular peak systolic velocity in healthy pediatric patients,
    calculation of z score, and comparison to tricuspid annular plane systolic excursion.''',
    'authors': '''Koestenberger M, Nagel B, Ravekes W, Avian A, Heinzl B, Cvirn G, Fritsch P,
    Fandl A, Rehak T, Gamillscheg A.''',
    'journal': 'Am J Cardiol. 2012 Jan 1;109(1):116-21.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/21944674'
}

class Base(object):
    '''
    This is the base class for the Koestenberger TAPSV data;
    lookup the nearest age in the ages list and use that index to get mean and
    SD values from the data list
    '''

    def __init__( self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.refName = 'koestenberger_ajc_2012'
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
    
    def zscore(self):
      if self.score >= self.mean():
        sd = (self.values[2] - self.mean()) / 2
      else:
        sd = (self.mean() - self.values[1]) / 2
      return (self.score - self.mean()) / sd

    def uln(self):
      sd = (self.values[2] - self.mean()) / 2
      return self.mean() + self.limit * sd
    
    def lln(self):
      sd = (self.mean() - self.values[1]) / 2
      return self.mean() - self.limit * sd

def getIndex(target):
  '''return the index of the age, used to lookup data values from the data list'''
  #set upper, lower limits
  if target < 0.08333:
    target = 0.08333
  if target > 18:
    target = 18
  # first see if there is an exact match, common for years > 1
  if target in ages:
      return ages.index(target)
    
  else:
    for i, j in enumerate(ages):
      if j > target:
          return i -1

# 
# individual site data 
#
ages = [
  #monthly thru 1 year; every year thereafter
  0.08333,
  0.1667,
  0.25,
  0.333,
  0.41667,
  0.5,
  0.58333,
  0.6667,
  0.75,
  0.8333,
  0.91667,
  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18
]
rv_tdi_s = { "name": "rv_tdi_s",
         'values': [
          #data are [mean, -2sd, +2sd]
          [7.2, 4.8, 9.5], #1mo
          [8.5, 6.5, 10.5],
          [8.7, 6.3, 11],
          [9.1, 6.3, 11.8],
          [9.8, 6.4, 13.2],
          [9.1, 7.5, 10.6], #6mo
          [9.5, 7.3, 11.8],
          [9.7, 6.4, 12.9],
          [9.9, 6.4, 13.4],
          [10.6, 9.1, 13.1],
          [11.1, 8.1, 14.1],
          [11.0, 7.7, 14.4], #1yr
          [11.4, 8.7, 14.0],
          [11.7, 8.3, 15.1],
          [12.2, 9.3, 15.0],
          [12.3, 9.4, 15.2],
          [12.4, 9.6, 15.3], #6yr
          [12.6, 9.7, 15.4],
          [12.7, 9.8, 15.6],
          [12.5, 9.5, 15.5],
          [12.8, 10.4, 15.2],
          [13.1, 10.3, 15.9],
          [12.9, 9.9, 16.4], #12yr
          [13.2, 10.7, 15.8],
          [13.3, 10.0, 17.7],
          [13.8, 10.5, 17.1],
          [14.1, 10.1, 18.1],
          [14.0, 10.1, 17.9],
          [14.3, 10.7, 17.9] #18yr
          ]}

sites = [
  'rv_tdi_s'
]
