#!/usr/bin/env python
# -*- coding: utf-8 -*-

import blanchard_msse_2018


zLimit = 1.96

REFS = {
    'blanchard-msse-2018': blanchard_msse_2018

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

    {'id': 'wlmax', 'long_name': 'Max Workload', 'short_name': 'Max Workload', 'units': 'watts',
     'landmark': 'Highest value at peak exercise'},
    {'id': 'wlvt', 'long_name': 'Workload at VT', 'short_name': 'Workload at VT', 'units': 'watts',
     'landmark': 'Workload at ventilatory anaerobic threshold'},
    {'id': 'vo2max', 'long_name': 'VO2 Max', 'short_name': 'VO2 Max', 'units': 'ml/min',
        'landmark': 'Highest recorded value of the VO2 averaged over 30 seconds during exercise'},
    {'id': 'vo2vt', 'long_name': 'VO2 at VT', 'short_name': 'VO2 at VT', 'units': 'ml/min',
        'landmark': 'Value of VO2 averaged for 30 seconds at ventilatory threshold'},
    {'id': 'pk02pulse', 'long_name': 'Peak O2 Pulse', 'short_name': 'Peak O2 Pulse', 'units': 'ml/beat',
        'landmark': 'VO2 / heart rate, highest recorded value averaged over 30 seconds during exercise'},
    {'id': 'vemax', 'long_name': 'Ve Max', 'short_name': 'Ve Max', 'units': 'L/min',
        'landmark': 'Highest recorded value averaged over 30 seconds during exercise'},
    {'id': 'pkrer', 'long_name': 'Peak RER', 'short_name': 'Peak RER', 'units': 'n/a',
        'landmark': 'VCO2 / VO2, highest recorded value averaged over 30 seconds during exercise'},
    {'id': 'hrmax', 'long_name': 'Max HR', 'short_name': 'Max HR', 'units': 'bpm',
        'landmark': 'Highest recorded value during exercise'},
    {'id': 'oues', 'long_name': 'OUES', 'short_name': 'OUES', 'units': 'n/a',
        'landmark': 'Slope of VO2 over Log10Ve (for the entire exercise phase)'},
    {'id': 'ouesvt', 'long_name': 'OUES below VT', 'short_name': 'OUES below VT', 'units': 'n/a',
         'landmark': 'Slope of VO2 over Log10Ve (from the start of exercise to ventilatory threshold)'},
    {'id': 'vevco2sl', 'long_name': 'Ve/VCO2 Slope', 'short_name': 'Ve/VCO2 Slope', 'units': 'n/a',
        'landmark': 'Slope of Ve over VCO2 (from the start of exercise to ventilatory threshold)'},
    {'id': 'vevco2slblwvt', 'long_name': 'Ve/VCO2 Slope below VT', 'short_name': 'Ve/VCO2 Slope below VT', 'units': 'n/a',
        'landmark': 'Ve over VCO2 (from the start of exercise to ventilatory threshold)'},
    {'id': 'vevco2slatvt', 'long_name': 'Ve/VCO2 Slope at VT', 'short_name': 'Ve/VCO2 Slope at VT', 'units': 'n/a',
        'landmark': 'Ve over VCO2 (value averaged over 30 seconds at ventilator threshold)'},
    {'id': 'o2pulseincr', 'long_name': 'O2 Pulse Increase', 'short_name': 'O2 Pulse Increase', 'units': '%',
         'landmark': 'Increase of O2 pulse during exercise compared to warm-up ([pk - avg dur wu] / avg dur wu)*100'},
    {'id': 'o2pulseslope', 'long_name': 'O2 Pulse/Workload Slope', 'short_name': 'O2 Pulse/Workload Slope', 'units': 'ml/bpm/watt',
        'landmark': 'Slope of O2pulse over workload (excluding the first 10% of exercise phase)'},
    {'id': 'vo2slope', 'long_name': 'VO2/Workload Slope', 'short_name': 'VO2/Workload Slope', 'units': 'ml/mim/watt',
        'landmark': 'Slope of VO2 over workload (excluding the first 10% of exercise phase)'},
    {'id': 'hrr1', 'long_name': 'Heart Rate Recovery 1 min', 'short_name': 'Heart Rate Recovery 1 min', 'units': 'bpm',
         'landmark': 'Heart rate after one minute of recovery'},
    {'id': 'hrr2', 'long_name': 'Heart Rate Recovery 2 min', 'short_name': 'Heart Rate Recovery 2 min', 'units': 'bpm',
        'landmark': 'Heart rate after two minutes of recovery'},

]



