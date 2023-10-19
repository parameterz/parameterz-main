#  !/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Haycock'

constraints = {'age': [0, '18y']}

name = 'Lopez et al., Circ Cardiovasc Imaging 2017'
description = 'Z-scores for Two Dimensional Echocardiographic Measurements Indexed to BSA using an Allometric Model'

detail = '''This is the data from the Pediatric Heart Network 'Echo Z-Score Project', a multi-year
 multi-institutional project, ultimately evaluating over 3200
patients &le; 18 years.

>BSA raised to a specified power is a good parameter for cardiovascular allometric scaling, and none of the
Z score models for the measurements in this study were affected by age, sex, race, or ethnicity.

'''
critique = {
    'model': 'allometric index',
    'subjects': 3215,
}

year = '2017'
citation = {
    'title': 'Relationship of Echocardiographic Z Scores Adjusted for Body Surface Area to Age, Sex, Race, and Ethnicity.',
    'authors': '''Lopez L, Colan S, Stylianou M, Granger S, Trachtenberg F, Frommelt P, Pearson
G, Camarda J, Cnota J, Cohen M, Dragulescu A, Frommelt M, Garuba O, Johnson T,
Lai W, Mahgerefteh J, Pignatelli R, Prakash A, Sachdeva R, Soriano B, Soslow J,
Spurney C, Srivastava S, Taylor C, Thankavel P, van der Velde M, Minich L;
Pediatric Heart Network Investigators''',
    'journal': 'Circ Cardiovasc Imaging. 2017 Nov;10(11). ',
    'url': 'https://www.ncbi.nlm.nih.gov/pubmed/29138232'
}


class Base(object):
    '''
    This is the base class for the Lopez/PHN data.
        The basic form of these equations is values indexed to BSA using an allometric exponent:
            z = [ ( parameter / BSA ^ x ) - mean value of indexed parameter ] /  sd of indexed parameter
    '''

    def __init__(self, data, pt, limit):
        self.source = name
        self.citation = citation
        self.siteName = data['name']
        self.refName = 'lopez_circimaging_2017'
        self.exponent = data['exp']
        self.imean = data['mean']  # the indexed mean
        self.isd = data['sd']  # the indexed sd
        self.limit = limit
        self.bsaMethod = bsaMethod
        self.bsa = pt.bsa(bsaMethod)
        self.score = float(getattr(pt, data['name']))
        self.constraints = constraints
        self.critique = critique
        self.exceptions = ['mv_area', 'tv_area', 'lmca', 'lad', 'prox_rca',
                           'lv_eda_psax', 'lv_eda_epi_psax', 'lvedv', 'lvedv_epi',
                           'lvm_2d', 'lv_mass_vol_ratio', 'lvpw_lvedd_ratio',
                           'lv_sphere_idx']  # do not convert as mm to cm


    def mean(self):
        indexedMean = self.imean
        actualMean = indexedMean * math.pow(self.bsa, self.exponent)
        actualMean = actualMean if self.siteName in self.exceptions else actualMean * 10
        return actualMean


    def zscore(self):
        score = self.score if self.siteName in self.exceptions else self.score/10
        mean = self.imean
        sd = self.isd

        try:
            return  (score / math.pow(self.bsa, self.exponent) - mean) / sd
        except:
            return None  # property of object 'pt' does not exist

    def uln(self):
        iLimit = self.imean + self.limit * self.isd
        actualLimit = iLimit * math.pow(self.bsa, self.exponent)
        actualLimit = actualLimit if self.siteName in self.exceptions else actualLimit * 10
        return actualLimit

    def lln(self):
        iLimit = self.imean - self.limit * self.isd
        actualLimit = iLimit * math.pow(self.bsa, self.exponent)
        actualLimit = actualLimit if self.siteName in self.exceptions else actualLimit * 10
        return actualLimit



#
# individual site data
#

mvd_ap = {'name': 'mvd_ap', 'exp': 0.50, 'mean': 2.31, 'sd': 0.24}
mvd_l = {'name': 'mvd_l', 'exp': 0.50, 'mean': 2.23, 'sd': 0.22}
mv_area = {'name': 'mv_area', 'exp': 1.00, 'mean': 4.06, 'sd': 0.68}
tvd_ap = {'name': 'tvd_ap', 'exp': 0.50, 'mean': 2.36, 'sd': 0.28}
tvd_l = {'name': 'tvd_l', 'exp': 0.50, 'mean': 2.36, 'sd': 0.29}
tv_area = {'name': 'tv_area', 'exp': 1.00, 'mean': 4.39, 'sd': 0.83}
aov = {'name': 'aov', 'exp': 0.50, 'mean': 1.48, 'sd': 0.14}
sov = {'name': 'sov', 'exp': 0.50, 'mean': 2.06, 'sd': 0.18}
stj = {'name': 'stj', 'exp': 0.50, 'mean': 1.69, 'sd': 0.16}
aao = {'name': 'aao', 'exp': 0.50, 'mean': 1.79, 'sd': 0.18}
prox_arch = {'name': 'prox_arch', 'exp': 0.50, 'mean': 1.53, 'sd': 0.23}
dist_arch = {'name': 'dist_arch', 'exp': 0.50, 'mean': 1.36, 'sd': 0.19}
isthmus = {'name': 'isthmus', 'exp': 0.50, 'mean': 1.25, 'sd': 0.18}
lmca = {'name': 'lmca', 'exp': 0.45, 'mean': 2.95, 'sd': 0.57}
lad = {'name': 'lad', 'exp': 0.45, 'mean': 1.90, 'sd': 0.34}
prox_rca = {'name': 'prox_rca', 'exp': 0.45, 'mean': 2.32, 'sd': 0.55}
pv = {'name': 'pv', 'exp': 0.50, 'mean': 1.91, 'sd': 0.24}
pv_plax = {'name': 'pv_plax', 'exp': 0.50, 'mean': 2.01, 'sd': 0.28}
mpa = {'name': 'mpa', 'exp': 0.50, 'mean': 1.82, 'sd': 0.24}
rpa = {'name': 'rpa', 'exp': 0.50, 'mean': 1.07, 'sd': 0.18}
lpa = {'name': 'lpa', 'exp': 0.50, 'mean': 1.10, 'sd': 0.18}
lvedd_psax = {'name': 'lvedd_psax', 'exp': 0.45, 'mean': 3.89, 'sd': 0.33}
lvpwd_psax = {'name': 'lvpwd_psax', 'exp': 0.40, 'mean': 0.57, 'sd': 0.09}
ivsd_psax = {'name': 'ivsd_psax', 'exp': 0.40, 'mean': 0.58, 'sd': 0.09}
lv_maj_ed_a4c = {'name': 'lv_maj_ed_a4c', 'exp': 0.45, 'mean': 6.31, 'sd': 0.46}
lv_maj_epi_ed_a4c = {'name': 'lv_maj_epi_ed_a4c', 'exp': 0.45, 'mean': 6.87, 'sd': 0.45}
lv_eda_psax = {'name': 'lv_eda_psax', 'exp': 0.90, 'mean': 11.91, 'sd': 1.89}
lv_eda_epi_psax = {'name': 'lv_eda_epi_psax', 'exp': 0.90, 'mean': 20.00, 'sd': 2.59}
lvedv = {'name': 'lvedv', 'exp': 1.3, 'mean': 62.02, 'sd': 11.94}
lvedv_epi = {'name': 'lvedv_epi', 'exp': 1.3, 'mean': 113.14, 'sd': 17.85}
lvm_2d = {'name': 'lvm_2d', 'exp': 1.25, 'mean': 53.02, 'sd': 9.06}
lv_mass_vol_ratio = {'name': 'lv_mass_vol_ratio', 'exp': 0, 'mean': 0.88, 'sd': 0.16}
lvpw_lvedd_ratio = {'name': 'lvpw_lvedd_ratio', 'exp': 0, 'mean': 0.15, 'sd': 0.03}
lv_sphere_idx = {'name': 'lv_sphere_idx', 'exp': 0, 'mean': 1.63, 'sd': 0.17}

sites = [
    'mvd_ap',
    'mvd_l',
    'mv_area',
    'tvd_ap',
    'tvd_l',
    'tv_area',
    'aov',
    'sov',
    'stj',
    'aao',
    'prox_arch',
    'dist_arch',
    'isthmus',
    'lmca',
    'lad',
    'prox_rca',
    'pv',
    'pv_plax',
    'mpa',
    'rpa',
    'lpa',
    'ivsd_psax',
    'lvedd_psax',
    'lvpwd_psax',
    'lv_maj_ed_a4c',
    'lv_maj_epi_ed_a4c',
    'lv_eda_psax',
    'lv_eda_epi_psax',
    'lvedv',
    'lvedv_epi',
    'lvm_2d',
    'lv_mass_vol_ratio',
    'lvpw_lvedd_ratio',
    'lv_sphere_idx'
]
