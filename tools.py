#!/usr/bin/env python

import webapp2
import views
import logging
import math
from lib import cdc_bmi, cdc_statage, cdc_wtage, patient
from calcs.echo import dallaire_jase_2011, kobayashi_jase_2016, mccrindle_circ_2007, olivieri_jase_2009

class ToolsHandler(views.BaseHandler):
    def get(self):
        self.render_template('/tools/index.html',
                            page = {"title": "Tools: Index Page",
                                   "description": "listing of available echo tools and applications"},
                            nav = TOOLS,
                           current_page = None)

        
class AVAToolHandler(views.BaseHandler):
    def get(self):
        self.render_template('/tools/aortic-valve-area-and-pressure-recovery.html',
                            page = {"title": "Tools: Aortic Valve Area and Pressure Recovery Calculator",
                                   "description": "Calculate Aortic Valve Area, Gradients, and Pressure Recovery"},
                            nav = TOOLS,
                            current_page = "aortic-valve-area-and-pressure-recovery")

class AOVSmackdownHandler(views.BaseHandler):
    def get(self):
        self.render_template('/tools/aortic-valve-smackdown.html',
                            page = {"title": "Tools: Aortic Valve Smackdown",
                                   "description": "Compare Aortic Valve Reference Ranges"},
                            nav = TOOLS,
                            current_page = "aortic-valve-smackdown")


class CASmackdownHandler(views.BaseHandler):
    def get(self):
        self.render_template('/tools/coronary-artery-smackdown.html',
                             page={"title": "Tools: Coronary Artery Smackdown",
                                   "description": "Compare Coronary Artery Reference Ranges"},
                             nav=TOOLS,
                             current_page="coronary-artery-smackdown")

class CAChartHandler(views.JSONBaseHandler):
    def get(self):
        result = []
        pt = patient.Patient()
        site = self.request.get('site')
        for msmt in ['ht', 'wt']:
            setattr( pt, msmt, float( self.request.get( msmt ) ) )
        setattr(pt, 'gender', self.request.get('gender'))

        diams = [x / 10.0 for x in range(5, 105, 5)]
        refs = [kobayashi_jase_2016, dallaire_jase_2011, mccrindle_circ_2007, olivieri_jase_2009]

        for diam in diams:
            setattr(pt, site, diam)
            temp = []
            temp.append(diam)
            for ref in refs:
                data = getattr(ref, site)
                base = ref.Base(data, pt, 1.96)
                temp.append(base.zscore())
            result.append(temp)

        # for ref in refs:
        #
        #     data = getattr(ref, site)
        #     for diam in diams:
        #         setattr(pt, site, diam)
        #         base = ref.Base(data, pt, 1.96)
        #         result[ref.name].append([diam, base.zscore()])


        self.renderJSON(result)



class BSAToolHandler(views.BaseHandler):
    def get(self):
        
            htData = {'boys': cdc_statage.boys, 'girls': cdc_statage.girls}
            wtData = {'boys': cdc_wtage.boys, 'girls': cdc_wtage.girls}
            #make a list for a table of BSA vs Ht/Wt/Age
            # [[bsa,age,ht,wt], [etc] ]
            boys = [[float(age), arr[1], wtData['boys'][age][1]] for age,arr in htData['boys'].items()]
            boys = [[calcHaycock(row[1], row[2]), row[0], row[1], row[2]] for row in boys]
            girls = [[float(age), arr[1], wtData['girls'][age][1]] for age,arr in htData['girls'].items()]
            girls = [[calcHaycock(row[1], row[2]), row[0], row[1], row[2]] for row in girls]
            self.render_template('/tools/bsa-ht-wt.html',
                                 page = {'title': 'Tools: estimate Ht/Wt',
                                         'description': 'use CDC data and growth curves to estimate height and weight from known BSA'},
                                 htData = htData,
                                 wtData = wtData,
                                 boysData = sorted(boys),
                                 girlsData = sorted(girls),
                                 nav = TOOLS,
                                 current_page = "bsa-ht-wt"
                                 )
            
class CVProfileToolHandler(views.BaseHandler):
    def get(self):
        self.render_template('/tools/chop-fetal-cv-profile.html',
                            page = {"title": "Tools: CHOP Fetal CV Profile Score",
                                   "description": "Fetal CV Profile Score used for assessing fetal TTTS"},
                            nav = TOOLS,
                            current_page = "chop-fetal-cv-profile")

            
def calcHaycock(ht, wt):
    return 0.024265 * math.pow(float(ht), 0.3964) * math.pow(float(wt), 0.5378)

TOOLS = {
    'bsa-ht-wt': {
    'title': 'BSA Tool',
    'description': 'reverse engineer height and weight from BSA',
    'intro': 'makes reasonable estimates of height and weight from known BSA'
    },
    'aortic-valve-area-and-pressure-recovery': {
    'title': 'AVA and Pressure Recovery',
    'description': 'calculate aortic valve area and pressure recovery',
    'intro': ''
    },
    'aortic-valve-smackdown': {
        'title': 'Aortic Valve Smackdown',
        'description': 'Compare Aortic Valve Reference Ranges',
        'intro': 'aortic valve smackdown: anniversary edition'
    },
    'coronary-artery-smackdown': {
        'title': 'Coronary Artery Smackdown',
        'description': 'Compare Coronary Artery Reference Ranges',
        'intro': 'coronary artery smackdown: Japanese Edition'
    },
    'chop-fetal-cv-profile': {
        'title': 'Fetal CV Profile Score',
        'description': 'The CHOP fetal CV Profile Score',
        'intro': 'Fetal CV Profile score, esp. for use with TTTS'
    }
    
}