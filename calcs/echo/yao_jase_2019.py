#  !/usr/bin/env python

from __future__ import division
import math

required = ['age', 'ht', 'wt']
bsaMethod = 'DuBois'

constraints = {'age': [18, '80y']}

name = 'Yao et al., J Am Soc Echo 2019'
description = 'Z-scores for Two Dimensional Echocardiographic Measurements using an Optimized Multivariable Allometric Model'

detail = '''This data is from a multi-institutional study enrolling over 1200 healthy, normal-weight, Chinese
Han ***adult*** volunteers, using a multivariable allometric model that controlled for body size as well as age.
Gender differences were completely removed for 32 of 34 of the parameters; when
applied to a group of overweight and obese patients, the success rate of correction using the model was 82.4%. (Reference
ranges are based on the ratio of measured/predicted).

>The goal of scaling cardiovascular dimensions is to remove the
physiologic influence of age, gender, and body size in individuals to
facilitate correct comparison and differentiation between normal
and abnormal values.

'''
critique = {
    'model': 'allometric ',
    'subjects': 1224,
}

year = '2019'
citation = {
    'title': 'A Novel Mathematical Model for Correcting the Physiologic Variance of Two-Dimensional Echocardiographic Measurements in Healthy Chinese Adults.',
    'authors': '''Yao GH, Chen XY, Zhang Q, Zeng XY, Li XL, Zhang S, Jiang PQ, Feng X, Sun FR,
Xu JF, Zhang M, Zhang C, Yin LX, Zhang M, Zhang Y.''',
    'journal': 'J Am Soc Echocardiogr. 2019 Apr 24.',
    'url': 'https://www.ncbi.nlm.nih.gov/pubmed/31029500'
}


class Base(object):
    '''
    This is the base class for the Yao OMAM data.
        The basic form of these equations is values raised to allometric exponents:
            predicted = a * Age^x * Ht^y * Wt^z
            The reference ranges are based on the ratio of "measured/predicted" (the "mean") and the SD of that ratio
    '''

    def __init__(self, data, pt, limit):
        self.source = name
        self.citation = citation
        self.siteName = data['name']
        self.refName = 'yao_jase_2019'
        self.constant = data['constant']
        self.a = data['a']
        self.h = data['h']
        self.w = data['w']
        self.m = data['mean']  # corrected value mean
        self.sd = data['sd']  # corrected value sd
        self.limit = limit
        self.age = float(pt.age)
        self.ht = float(pt.ht)
        self.wt = float(pt.wt)
        self.score = float(getattr(pt, data['name']))
        self.constraints = constraints
        self.critique = critique

    def predicted(self):
        p = self.constant
        p = p * math.pow(self.age, self.a)
        p = p * math.pow(self.wt, self.w)
        p = p * math.pow(self.ht, self.h)
        return p

    def mean(self):
        return self.m * self.predicted()

    def corrected(self):
        return self.score / self.predicted()

    def zscore(self):
        score = self.corrected()
        mean = self.m
        sd = self.sd

        try:
            return (score - mean) / sd
        except:
            return None  # property of object 'pt' does not exist

    def uln(self):
        # the published mean and sd are for the corrected values
        y = self.m + self.limit * self.sd
        upper = self.predicted() * y
        return upper

    def lln(self):
        # the published mean and sd are for the corrected values
        y = self.m - self.limit * self.sd
        lower = self.predicted() * y
        return lower


#
# individual site data
#

la = {'name': 'la', 'constant': 19.24, 'a': 0.093, 'w': 0.399, 'h': -0.304, 'mean': 1.011, 'sd': 0.127}
la_major_a4c = {'name': 'la_major_a4c', 'constant': 54.49, 'a': 0.079, 'w': 0.298, 'h': -0.334, 'mean': 1.014, 'sd': 0.118}
la_minor_a4c = {'name': 'la_minor_a4c', 'constant': 14.82, 'a': 0.032, 'w': 0.179, 'h': 0, 'mean': 0.996, 'sd': 0.129}
la_area_a4c = {'name': 'la_area_a4c', 'constant': 2.20, 'a': 0.132, 'w': 0.326, 'h': 0, 'mean': 1.034, 'sd': 0.213}
lav = {'name': 'lav', 'constant': 2.03, 'a': 0.173, 'w': 0.528, 'h': 0, 'mean': 1.056, 'sd': 0.315}
lvot_nos = {'name': 'lvot_nos', 'constant': 0.80, 'a': 0, 'w': 0.202, 'h': 0.449, 'mean': 1.012, 'sd': 0.158}
ivsd_plax = {'name': 'ivsd_plax', 'constant': 1.18, 'a': 0.133, 'w': 0.356, 'h': 0, 'mean': 1.010, 'sd': 0.141}
ivss_plax = {'name': 'ivss_plax', 'constant': 1.96, 'a': 0.141, 'w': 0.310, 'h': 0, 'mean': 0.999, 'sd': 0.143}
lvpwd_plax = {'name': 'lvpwd_plax', 'constant': 1.18, 'a': 0.122, 'w': 0.358, 'h': 0, 'mean': 1.017, 'sd': 0.145}
lvpws_plax = {'name': 'lvpws_plax', 'constant': 2.88, 'a': 0.111, 'w': 0.245, 'h': 0, 'mean': 1.007, 'sd': 0.144}
lvedd_plax = {'name': 'lvedd_plax', 'constant': 14.63, 'a': 0, 'w': 0.271, 'h': 0, 'mean': 1.003, 'sd': 0.081}
lvesd_plax = {'name': 'lvesd_plax', 'constant': 7.58, 'a': -0.046, 'w': 0.369, 'h': 0, 'mean': 1.011, 'sd': 0.125}
lvedv = {'name': 'lvedv', 'constant': 0.05, 'a': -0.069, 'w': 0.466, 'h': 1.097, 'mean': 1.032, 'sd': 0.231}
lvesv = {'name': 'lvesv', 'constant': 0.008, 'a': -0.122, 'w': 0.481, 'h': 1.294, 'mean': 1.051, 'sd': 0.358}
lvef = {'name': 'lvef', 'constant': 128, 'a': 0.027, 'w': 0, 'h': -0.155, 'mean': 1.010, 'sd': 0.097}
lvm_2d = {'name': 'lvm_2d', 'constant': 1.32, 'a': 0.153, 'w': 0.954, 'h': 0, 'mean': 1.020, 'sd': 0.228}
aov_d = {'name': 'aov_d', 'constant': 0.98, 'a': 0.061, 'w': 0.203, 'h': 0.385, 'mean': 1.004, 'sd': 0.112}
sov_d = {'name': 'sov_d', 'constant': 0.73, 'a': 0.106, 'w': 0.201, 'h': 0.478, 'mean': 1.002, 'sd': 0.111}
aao_d = {'name': 'aao_d', 'constant': 4.38, 'a': 0.155, 'w': 0.297, 'h': 0, 'mean': 0.995, 'sd': 0.124}
arch_nos = {'name': 'arch_nos', 'constant': 3.79, 'a': 0.147, 'w': 0.311, 'h': 0, 'mean': 1.013, 'sd': 0.140}
dao_nos = {'name': 'dao_nos', 'constant': 3.36, 'a': 0.157, 'w': 0.279, 'h': 0, 'mean': 1.015, 'sd': 0.176}
pv_d = {'name': 'pv_d', 'constant': 5.41, 'a': 0.053, 'w': 0.262, 'h': 0, 'mean': 1.013, 'sd': 0.163}
mpa_d = {'name': 'mpa_d', 'constant': 6.36, 'a': 0.071, 'w': 0.218, 'h': 0, 'mean': 1.006, 'sd': 0.144}
rpa_d = {'name': 'rpa_d', 'constant': 2.31, 'a': 0.116, 'w': 0.295, 'h': 0, 'mean': 1.013, 'sd': 0.206}
lpa_d = {'name': 'lpa_d', 'constant': 2.62, 'a': 0.123, 'w': 0.264, 'h': 0, 'mean': 1.012, 'sd': 0.189}
ra_major_a4c = {'name': 'ra_major_a4c', 'constant': 8.27, 'a': 0.087, 'w': 0.319, 'h': 0, 'mean': 1.016, 'sd': 0.102}
ra_minor_a4c = {'name': 'ra_minor_a4c', 'constant': 8.08, 'a': 0, 'w': 0.346, 'h': 0, 'mean': 1.011, 'sd': 0.134}
rv_awt = {'name': 'rv_awt', 'constant': 1.36, 'a': 0.128, 'w': 0.143, 'h': 0, 'mean': 1.009, 'sd': 0.223}
rv_fwt = {'name': 'rv_fwt', 'constant': 1.18, 'a': 0.057, 'w': 0.256, 'h': 0, 'mean': 1.045, 'sd': 0.271}
rvot_psax = {'name': 'rvot_psax', 'constant': 8.66, 'a': 0, 'w': 0.231, 'h': 0, 'mean': 1.020, 'sd': 0.182}
rv_ap_plax = {'name': 'rv_ap_plax', 'constant': 6.12, 'a': 0.081, 'w': 0.230, 'h': 0, 'mean': 1.027, 'sd': 0.170}
rv_len = {'name': 'rv_len', 'constant': 20.13, 'a': -0.037, 'w': 0.270, 'h': 0, 'mean': 1.026, 'sd': 0.171}
rv_mc_a4c = {'name': 'rv_mc_a4c', 'constant': 4.92, 'a': 0, 'w': 0.394, 'h': 0, 'mean': 1.015, 'sd': 0.198}
rv_b_a4c = {'name': 'rv_b_a4c', 'constant': 5.24, 'a': 0.056, 'w': 0.376, 'h': 0, 'mean': 1.020, 'sd': 0.164}





sites = [
    'la',
    'ivsd_plax',
    'ivss_plax',
    'lvedd_plax',
    'lvpwd_plax',
    'lvpws_plax',
    'lvesd_plax',
    'lav',
    'lvedv',
    'lvesv',
    'lvef',
    'lvm_2d',
    'aov_d',
    'sov_d',
    'aao_d',
    'pv_d',
    'mpa_d',
    'rpa_d',
    'lpa_d',
    'rv_len',
    'rv_b_a4c',
    'rv_mc_a4c',
    'ra_major_a4c',
    'ra_minor_a4c',
    'la_major_a4c',
    'la_minor_a4c',
    'la_area_a4c',
    'rv_awt',
    'rv_fwt',
    'rv_ap_plax',
    'rvot_psax',
    'lvot_nos',
    'arch_nos',
    'dao_nos'

]
