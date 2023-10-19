#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import math
import logging

required = ['wt', 'gender']
constraints = {'wt': [0.4, 2.0]}

name = 'Choudhry et al., JASE 2017'
description = '''LV M-mode z-scores for premature infants up to 2 kg'''
detail = '''Gender-specific, weight-adjusted z-scores of left ventricular m-mode measurements (including LV mass) for
use on premature babies up to 2 kg.

> Because weight is a practical measurement in preterm infants and our analysis found that length or BSA were not
superior indexes, we propose that weight be used as the index for LV dimensions in small premature infants.

'''
citation = {
    'title': 'Normative Left Ventricular M-Mode Echocardiographic Values in Preterm Infants up to 2 kg.',
    'authors': 'Choudhry S, Salter A, Cunningham TW, Levy PT, Nguyen HH, Wallendorf M, Singh GK, Johnson MC.',
    'journal': 'J Am Soc Echocardiogr. 2017 Jun 6. pii:S0894-7317(17)30355-3.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/28599830'
}
class Base(object):
    ''' This is the base class for the Choudry et al model.
        These are all LMS lookups.
        '''

    def __init__(self, data, pt, limit):
        self.source = name
        self.citation = citation
        self.refName = 'choudhry_jase_2017'
        self.siteName = data['name']
        self.wt = float(pt.wt)
        self.gender = pt.gender
        self.lms = data[pt.gender]
        self.limit = limit
        self.score = float(getattr(pt, data['name']))
        self.constraints = constraints
        # chart stuff
        self.chartData = False

    def getIndex(self, wt):
        if wt < 0.4:
            wt = 0.4
        if wt > 2.0:
            wt = 2.0
        if wt in wtRange:
            return wtRange.index(wt)
        else:
            return None

    def getLMS(self, wt):
        # first see if the index is found w/ getIndex()
        # if not, get the nearest value
        # min(myList, key=lambda x:abs(x-myNumber))
        # and interpolate

        if self.getIndex(wt) is not None:

            return self.lms[self.getIndex(wt)]

        else:
            nextWt = next(x for x in wtRange if x > wt)
            hiIndex = wtRange.index(nextWt)
            loIndex = hiIndex - 1
            # figure out what the delta of the listed wt vs pt wt; for use in interpolating the LMS values
            minWt = nextWt - 0.1
            delta = wt - minWt  # delta above the lower listed wt
            percent = delta / 0.1  # the percent above the lower listed BSA; '0.1' is the step between listed wts
            lo = self.lms[loIndex]
            hi = self.lms[hiIndex]
            l = (hi[0] - lo[0]) * percent + lo[0]
            m = (hi[1] - lo[1]) * percent + lo[1]
            s = (hi[2] - lo[2]) * percent + lo[2]

            return [l, m, s]

    def _mean(self, wt):
        # the 'M' in 'LMS'!
        return self.getLMS(wt)[1]

    def mean(self):
        return self._mean(self.wt) if self.siteName == "lvm_mm" else self._mean(self.wt)*10

    def zscore(self):
        lms = self.getLMS(self.wt)
        l = lms[0]
        m = lms[1]
        s = lms[2]
        score = self.score if self.siteName == "lvm_mm" else self.score/10
        z = ((math.pow(score / m, l) - 1) / (l * s))
        return z


    def _uln(self, wt):
        lms = self.getLMS(wt)
        l = lms[0]
        m = lms[1]
        s = lms[2]
        # calculate the uln
        limit = self.limit * l * s
        limit += 1
        return math.pow(limit, (1 / l)) * m

    def _lln(self, wt):
        lms = self.getLMS(wt)
        l = lms[0]
        m = lms[1]
        s = lms[2]
        # calculate the uln
        limit = -self.limit * l * s
        limit += 1
        return math.pow(limit, (1 / l)) * m

    def uln(self):
        return self._uln(self.wt) if self.siteName == "lvm_mm" else self._uln(self.wt) * 10

    def lln(self):
        return self._lln(self.wt) if self.siteName == "lvm_mm" else self._lln(self.wt) * 10


wtRange = [
    0.4,
    0.5,
    0.6,
    0.7,
    0.8,
    0.9,
    1.0,
    1.1,
    1.2,
    1.3,
    1.4,
    1.5,
    1.6,
    1.7,
    1.8,
    1.9,
    2.0
]

# l,m,s values
lvm_mm = {'name': 'lvm_mm',
          'f': [
              [1.741, 1.586, 0.2],
              [1.349, 1.875, 0.199],
              [0.954, 2.164, 0.197],
              [0.554, 2.453, 0.196],
              [0.14, 2.742, 0.195],
              [-0.289, 3.031, 0.194],
              [-0.687, 3.319, 0.192],
              [-0.989, 3.608, 0.191],
              [-1.157, 3.897, 0.19],
              [-1.215, 4.186, 0.189],
              [-1.206, 4.475, 0.187],
              [-1.167, 4.764, 0.186],
              [-1.132, 5.053, 0.185],
              [-1.118, 5.341, 0.184],
              [-1.117, 5.63, 0.183],
              [-1.121, 5.919, 0.181],
              [-1.122, 6.208, 0.18]],
          'm': [
              [-0.563, 1.366, 0.257],
              [-0.492, 1.729, 0.246],
              [-0.420, 2.092, 0.236],
              [-0.348, 2.456, 0.225],
              [-0.277, 2.823, 0.214],
              [-0.205, 3.200, 0.202],
              [-0.134, 3.583, 0.190],
              [-0.062, 3.958, 0.178],
              [0.009, 4.318, 0.168],
              [0.081, 4.663, 0.160],
              [0.152, 4.992, 0.155],
              [0.224, 5.305, 0.151],
              [0.295, 5.603, 0.149],
              [0.367, 5.889, 0.148],
              [0.438, 6.164, 0.148],
              [0.510, 6.430, 0.149],
              [0.581, 6.690, 0.151]
          ]}

ivsd_mm = {'name': 'ivsd_mm',
           'm': [
               [0.389, 0.194, 0.195],
               [0.268, 0.204, 0.188],
               [0.146, 0.214, 0.182],
               [0.025, 0.225, 0.175],
               [-0.097, 0.235, 0.169],
               [-0.218, 0.244, 0.164],
               [-0.340, 0.253, 0.158],
               [-0.461, 0.262, 0.153],
               [-0.582, 0.269, 0.147],
               [-0.704, 0.277, 0.142],
               [-0.825, 0.283, 0.137],
               [-0.947, 0.289, 0.133],
               [-1.068, 0.294, 0.128],
               [-1.190, 0.298, 0.124],
               [-1.311, 0.300, 0.120],
               [-1.432, 0.302, 0.115],
               [-1.554, 0.303, 0.111],
           ],
           'f': [
               [-0.924, 0.185, 0.184],
               [-0.842, 0.195, 0.179],
               [-0.76, 0.205, 0.175],
               [-0.677, 0.214, 0.17],
               [-0.595, 0.224, 0.164],
               [-0.513, 0.234, 0.158],
               [-0.43, 0.243, 0.152],
               [-0.348, 0.252, 0.147],
               [-0.266, 0.26, 0.141],
               [-0.184, 0.268, 0.137],
               [-0.101, 0.275, 0.134],
               [-0.019, 0.282, 0.131],
               [0.063, 0.289, 0.13],
               [0.146, 0.295, 0.129],
               [0.228, 0.301, 0.129],
               [0.31, 0.307, 0.128],
               [0.393, 0.312, 0.128],
           ]}

lvpwd_mm = {
    'name': 'lvpwd_mm',
    'm': [
        [-0.737, 0.173, 0.207],
        [-0.608, 0.182, 0.190],
        [-0.479, 0.190, 0.173],
        [-0.350, 0.199, 0.157],
        [-0.221, 0.207, 0.143],
        [-0.092, 0.215, 0.131],
        [0.037, 0.224, 0.122],
        [0.167, 0.235, 0.118],
        [0.296, 0.246, 0.116],
        [0.425, 0.258, 0.118],
        [0.554, 0.268, 0.121],
        [0.683, 0.274, 0.124],
        [0.812, 0.278, 0.126],
        [0.941, 0.279, 0.127],
        [1.070, 0.278, 0.125],
        [1.199, 0.277, 0.122],
        [1.328, 0.275, 0.118]
    ],
    'f': [
        [-0.85, 0.17, 0.155],
        [-0.779, 0.18, 0.154],
        [-0.708, 0.19, 0.153],
        [-0.637, 0.199, 0.151],
        [-0.566, 0.209, 0.148],
        [-0.495, 0.218, 0.143],
        [-0.424, 0.227, 0.138],
        [-0.353, 0.235, 0.132],
        [-0.282, 0.243, 0.127],
        [-0.211, 0.25, 0.123],
        [-0.14, 0.256, 0.121],
        [-0.068, 0.262, 0.12],
        [0.003, 0.267, 0.121],
        [0.074, 0.271, 0.123],
        [0.145, 0.275, 0.126],
        [0.216, 0.279, 0.129],
        [0.287, 0.283, 0.132]
    ]
}

lvedd_mm = {
    'name': 'lvedd_mm',
    'm': [
        [-0.807, 0.847, 0.151],
        [-0.764, 0.924, 0.144],
        [-0.721, 1.001, 0.138],
        [-0.677, 1.078, 0.132],
        [-0.634, 1.157, 0.127],
        [-0.591, 1.240, 0.121],
        [-0.548, 1.317, 0.116],
        [-0.504, 1.382, 0.112],
        [-0.461, 1.435, 0.107],
        [-0.418, 1.479, 0.103],
        [-0.374, 1.514, 0.100],
        [-0.331, 1.541, 0.096],
        [-0.288, 1.566, 0.093],
        [-0.244, 1.595, 0.090],
        [-0.201, 1.632, 0.087],
        [-0.158, 1.675, 0.084],
        [-0.115, 1.720, 0.081]
    ],
    'f': [
        [0.752, 0.9, 0.14],
        [0.639, 0.968, 0.137],
        [0.525, 1.035, 0.133],
        [0.412, 1.101, 0.13],
        [0.299, 1.167, 0.126],
        [0.185, 1.23, 0.123],
        [0.072, 1.285, 0.12],
        [-0.042, 1.331, 0.117],
        [-0.155, 1.371, 0.114],
        [-0.268, 1.406, 0.111],
        [-0.382, 1.439, 0.108],
        [-0.495, 1.473, 0.105],
        [-0.609, 1.511, 0.103],
        [-0.722, 1.555, 0.1],
        [-0.835, 1.601, 0.097],
        [-0.949, 1.649, 0.095],
        [-1.062, 1.697, 0.092]
    ]
}

lvesd_mm = {
    'name': 'lvesd_mm',
    'm': [
        [1, 0.548, 0.120],
        [1, 0.599, 0.120],
        [1, 0.649, 0.119],
        [1, 0.701, 0.119],
        [1, 0.757, 0.119],
        [1, 0.816, 0.118],
        [1, 0.868, 0.118],
        [1, 0.907, 0.118],
        [1, 0.933, 0.117],
        [1, 0.951, 0.117],
        [1, 0.967, 0.116],
        [1, 0.983, 0.116],
        [1, 1.003, 0.116],
        [1, 1.030, 0.115],
        [1, 1.062, 0.115],
        [1, 1.098, 0.115],
        [1, 1.135, 0.114]
    ],
    'f': [
        [0.72, 0.577, 0.206],
        [0.649, 0.618, 0.197],
        [0.577, 0.661, 0.189],
        [0.506, 0.706, 0.181],
        [0.435, 0.751, 0.174],
        [0.363, 0.794, 0.167],
        [0.292, 0.83, 0.16],
        [0.22, 0.859, 0.153],
        [0.149, 0.884, 0.147],
        [0.078, 0.905, 0.141],
        [0.006, 0.927, 0.135],
        [-0.065, 0.955, 0.13],
        [-0.136, 0.989, 0.125],
        [-0.208, 1.025, 0.119],
        [-0.279, 1.059, 0.115],
        [-0.351, 1.091, 0.11],
        [-0.422, 1.121, 0.105]
    ]
}

sites = [
    'ivsd_mm',
    'lvedd_mm',
    'lvpwd_mm',
    'lvesd_mm',
    'lvm_mm'

]