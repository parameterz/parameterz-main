#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jcmr08
import ijci11
import jcmr09

zLimit = 1.96

REFS = {
    'jcmr08': jcmr08,
    'ijci11': ijci11,
    'jcmr09': jcmr09,
}
'''
all inputs as a list, to preserve order
this is a hand-built list and must match all the sites and references

site = {'id': '', #for generating html inputs (name/id)
        'short_name': '', #for input labels
        'long_name': '', #for report/page titles
        'timing': '', #systole or diastole
        'units': '', #mm, ml, cm/sec, etc.
        'landmark': '', #'leaflet hinge points', 'anterior to RPA', etc
        'category': '', #one of [Atria, Aorta, AV Valves, etc]
        'modality': '', #one of [M-Mode, 2D, Doppler, etc]
        }
'''
INPUTS = [

            {'id': 'sov', 'short_name': 'Sinus of Valsalva', 'units': 'mm'},
            {'id': 'stj', 'short_name': 'Sino-Tubular Junction', 'units': 'mm'},
            {'id': 'aao', 'short_name': 'Ascending Aorta', 'units': 'mm'},
            {'id': 'bca', 'short_name': '1st Brachiocephalic Origin', 'units': 'mm'},
            {'id': 't1', 'short_name': 'Proximal Transverse Arch', 'units': 'mm'},
            {'id': 't2', 'short_name': 'Distal Transverse Arch', 'units': 'mm'},
            {'id': 'isth', 'short_name': 'Isthmus', 'units': 'mm'},
            {'id': 'dao', 'short_name': 'Descending Aorta', 'units': 'mm'},
            {'id': 'diaph', 'short_name': 'Aorta at Diaphragm', 'units': 'mm'},
            {'id': 'mpa_axial', 'short_name': 'MPA, Axial', 'units': 'mm'},
            {'id': 'mpa_sagittal', 'short_name': 'MPA, Sagittal', 'units': 'mm'},
            {'id': 'rpa_prox_axial', 'short_name': 'RPA, Proximal, Axial', 'units': 'mm'},
            {'id': 'rpa_dist_axial', 'short_name': 'RPA, Distal, Axial', 'units': 'mm'},
            {'id': 'rpa_prox_rao', 'short_name': 'RPA, Proximal, RAO', 'units': 'mm'},
            {'id': 'rpa_dist_rao', 'short_name': 'RPA, Distal, RAO', 'units': 'mm'},
            {'id': 'lpa_prox_axial', 'short_name': 'LPA, Proximal, Axial', 'units': 'mm'},
            {'id': 'lpa_dist_axial', 'short_name': 'LPA, Distal, Axial', 'units': 'mm'},
            {'id': 'lpa_prox_lao', 'short_name': 'LPA, Proximal, LAO', 'units': 'mm'},
            {'id': 'lpa_dist_lao', 'short_name': 'LPA, Distal, LAO', 'units': 'mm'},
            {'id': 'lvedv', 'short_name': 'LV End Diastolic Volume', 'units': 'ml'},
            {'id': 'lvesv', 'short_name': 'LV End Systolic Volume', 'units': 'ml'},
            {'id': 'lvsv', 'short_name': 'LV Stroke Volume', 'units': 'ml'},
            {'id': 'lvco', 'short_name': 'LV Cardiac Output', 'units': 'ml/min'},
            {'id': 'lvm', 'short_name': 'LV Mass', 'units': 'g'},
            {'id': 'paps', 'short_name': 'Papillary Muscles', 'units': 'g'},
            {'id': 'rvedv', 'short_name': 'RV End Diastolic Volume', 'units': 'ml'},
            {'id': 'rvesv', 'short_name': 'RV End Systolic Volume', 'units': 'ml'},
            {'id': 'rvsv', 'short_name': 'RV Stroke Volume', 'units': 'ml'},
            {'id': 'rvco', 'short_name': 'RV Cardiac Output', 'units': 'ml/min'},
            {'id': 'rvm', 'short_name': 'RV Mass', 'units': 'g'},

]
        


