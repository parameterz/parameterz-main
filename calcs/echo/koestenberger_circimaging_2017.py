#  !/usr/bin/env python

from __future__ import division
import math

required = ['age', 'gender']

constraints = {'age': [0, '18y']}

name = 'Koestenberger et al., Circ Cardiovasc Imaging 2017'
description = 'z-scores of the pulmonary artery acceleration time (PAAT)'

detail = '''Age and Gender-adjusted z-scores of the pulmonary artery acceleration time.

>Abnormal PAAT values with scores < -2 were predictive of PH.
'''

critique = {
    'model': 'nonlinear realtionship with age',
    'subjects': 756,
    'heterosc': True,
    'residual_assoc': True,
    'residual_heterosc': True,
    'distribution': True,
    'source': 'source article'
}
year = '2017'
citation = {
    'title': 'Normal Reference Values and z Scores of the Pulmonary Artery Acceleration Time in Children and Its Importance for the Assessment of Pulmonary Hypertension.',
    'authors': 'Koestenberger M, Grangl G, Avian A, Gamillscheg A, Grillitsch M, Cvirn G, Burmas A, Hansmann G.',
    'journal': 'Circ Cardiovasc Imaging. 2017 Jan;10(1)',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/28003222'
}


class Base(object):
    '''
    This is the base class for the Koestenberger PAAT data.
    '''

    def __init__(self, data, pt, limit):
        self.source = name
        self.citation = citation
        self.refName = 'koestenberger_circimaging_2017'
        self.siteName = 'Pulm Art Accel Time'
        self.age = float(pt.age)
        self.gender = pt.gender
        self.limit = limit
        self.score = float(getattr(pt, data['name']))
        # chart stuff
        self.chartData = False
        # self.bsaData = [x * 0.1 for x in range(1, 7)] #bsa range is 0.12-0.67
        # self.chartXAxisLabel = 'BSA'
        # self.myData = ( [[self.bsa, self.score]] )#plot data
        self.constraints = constraints
        self.critique = critique

    def mean(self):
        g = 1 if self.gender in ['female', 'f', 'Female', 'F'] else 0
        age = self.age
        return 77.38 + 0.72 * age + 13.88 * math.sqrt(age) + 2.02 * g

    def sd(self):
        age = self.age
        return 12.87 + 0.17 * age

    def zscore(self):
        return ( self.score - self.mean() ) / self.sd()

    def uln(self):
        z = self.limit
        return self.mean() + z * self.sd()

    def lln(self):
        z = self.limit
        return self.mean() - z * self.sd()

paat = { 'name': 'paat' }

sites = [

    'paat'
]
