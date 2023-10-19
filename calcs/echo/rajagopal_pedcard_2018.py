#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa', 'gender']
bsaMethod = 'Haycock'
constraints = {'age': [0, 18], 'bsa': [0.19, 2.05]}

name = 'Rajagopal et al., Ped Card 2018'
year = '2018'
description = 'BSA-adjusted z-scores for planimetered apical 4-chamber right atrial area.'

detail = '''BSA-adjusted z-scores of right atrial area, measured using planimetry/tracing. Areas are adjusted for body size using allometric
equations (allometric exponents are different for children on either side of 1m<sup>2</sup>).

>We hope that this study will pave way for a gradual paradigm shift to more quantitative approaches for the assessment
of RA size and allow clinicians to better incorporate assessment of the right heart into an echocardiographic evaluation.

'''

critique = {
    'model': 'Indexed to BSA<sup>0.95</sup> or to BSA<sup>0.88</sup> (allometric model)',
    'subjects': 300,
    'heterosc': True,
    'residual_assoc': True,
    'residual_heterosc': True,
    'distribution': True,
    'source': 'parameterz'
}

citation = {
    'title': 'Validation of Right Atrial Area as a Measure of Right Atrial Size and Normal Values of in Healthy Pediatric Population by Two-Dimensional Echocardiography.',
    'authors': 'Rajagopal H, Uppu SC, Weigand J, Lee S, Karnik R, Ko H, Bhatla P, Nielsen J, Doucette J, Parness I, Srivastava S.',
    'journal': 'Pediatr Cardiol. 2018 Jun;39(5):892-901.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/29523923'
}


class Base(object):
    '''
    This is the base class for the Rajagopal RA Area calculations, similar to the Bhatla et al LA vol calcs

    '''

    def __init__(self, data, pt, limit):
        self.source = name
        self.citation = citation
        self.siteName = data['name']
        self.refName = 'rajagopal_pedcard_2018'
        self.limit = limit
        self.bsaMethod = bsaMethod
        self.bsa = pt.bsa(bsaMethod)
        self.gender = pt.gender
        self.score = float(getattr(pt, data['name']))
        # chart stuff
        self.chartData = True
        self.chartXAxisLabel = 'BSA'
        self.myData = ([[self.bsa, self.score]])  # plot data
        self.constraints = constraints
        self.critique = critique

    def mean(self):
        if self.bsa <= 1.0:
            # ae = 0.95
            return 9.7 * math.pow(self.bsa, 0.95)
        else:
            # ae = 0.88
            indexed_mean = 9.7 if self.gender == 'm' else 8.45
            return indexed_mean * math.pow(self.bsa, 0.88)



    def zscore(self):
        if self.bsa <= 1.0:
            # transform RA area into 'indexed' value
            # ae = 0.95
            score = self.score / math.pow(self.bsa, 0.95)
            mean = 9.7
            sd = 1.3
            return (score - mean) / sd
        else:
            # transform area into 'indexed' value
            # ae = 0.88
            score = self.score / math.pow(self.bsa, 0.88)
            mean = 9.7 if self.gender == 'm' else 8.45
            sd = 1.4 if self.gender == 'm' else 1.1
            return (score - mean) / sd

    def lln(self):
        ae = 0
        sd = 0
        indexed_mean = 0
        if self.bsa <= 1.0:
            ae = 0.95
            indexed_mean = 9.7
            sd = 1.3
        else:
            ae = 0.88
            indexed_mean = 9.7 if self.gender == 'm' else 8.45
            sd = 1.4 if self.gender == 'm' else 1.1

        return (indexed_mean - sd * self.limit) * math.pow(self.bsa, ae)

    def uln(self):
        ae = 0
        sd = 0
        indexed_mean = 0
        if self.bsa <= 1.0:
            ae = 0.95
            indexed_mean = 9.7
            sd = 1.3
        else:
            ae = 0.88
            indexed_mean = 9.7 if self.gender == 'm' else 8.45
            sd = 1.4 if self.gender == 'm' else 1.1

        return (indexed_mean + sd * self.limit) * math.pow(self.bsa, ae)




#
# individual site data
#

ra_area_a4c = {'name': 'ra_area_a4c'}

sites = [
    'ra_area_a4c'
]
