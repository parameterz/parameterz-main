#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import views
import err
import echo
import cmr
import phn
import exercise
import news
import tools
from webapp2_extras.routes import RedirectRoute
from lib import markdown

def md_to_html(content):
    ''' a Jinja2 filter to convert markdown to html
        using markdown: http://pythonhosted.org/Markdown/index.html
        
        Tips on getting it up and running:
        http://stackoverflow.com/questions/8039925/adding-a-custom-jinja2-filter-in-gae-1-6-0#answer-15341672
        https://groups.google.com/forum/#!topic/pocoo-libs/xwYo5Vh-o5M
        https://bitbucket.org/abernier/yab (models.py uses markdown)
    '''
    if content:
        content_html = markdown.markdown(content, extensions=['lib.markdown.extensions.footnotes'], output_format='html5')
        return content_html
    else:
        return 0

myconfig = {'webapp2_extras.jinja2': {'template_path': ['templates','news'],
                                      'filters': {'markdown': md_to_html}}
}

_routes = [
    (RedirectRoute(r'/refs/<ref>', handler=echo.RefHandler, strict_slash=True, name="ref")),
    (RedirectRoute(r'/refs/', handler=echo.RefsHandler, strict_slash=True, name="refs home")),
    (RedirectRoute(r'/sites/<site>', handler=echo.SiteHandler, strict_slash=True, name="site")),
    (RedirectRoute(r'/sites/', handler=echo.SitesHandler, strict_slash=True, name="sites home")),
    (RedirectRoute(r'/news/<year>/<month>/<day>/<title>', handler=news.ViewArticle, strict_slash=True, name="news article")),
    (RedirectRoute(r'/news/changelog', handler=news.Changelog, strict_slash=True, name="changelog")),
    (RedirectRoute(r'/news/', handler=news.Index, strict_slash=True, name="news home")),
    (RedirectRoute(r'/tools/', handler=tools.ToolsHandler, strict_slash=True, name="Tools home")),
    (RedirectRoute(r'/tools/bsa-ht-wt', handler=tools.BSAToolHandler, strict_slash=True, name="BSA tool")),
    (RedirectRoute(r'/tools/aortic-valve-area-and-pressure-recovery', handler=tools.AVAToolHandler, strict_slash=True, name="AVA tool")),
    (RedirectRoute(r'/tools/aortic-valve-smackdown', handler=tools.AOVSmackdownHandler, strict_slash=True, name="AOV smackdown tool")),
    (RedirectRoute(r'/tools/coronary-artery-smackdown', handler=tools.CASmackdownHandler, strict_slash=True, name="CA smackdown tool")),
    (RedirectRoute(r'/tools/chart-data', handler=tools.CAChartHandler, strict_slash=True, name='CA Chart Data')),
    (RedirectRoute(r'/tools/chop-fetal-cv-profile', handler=tools.CVProfileToolHandler, strict_slash=True, name="CV Profile Score tool")),
    (RedirectRoute(r'/methods', handler=echo.MethodsHandler, strict_slash=True, name="methods")),
    (RedirectRoute(r'/disclaimer', handler=views.disclaimerHandler, strict_slash=True, name="disclaimer")),
    (RedirectRoute(r'/about', handler=views.AboutHandler, strict_slash=True, name="about")),
    (RedirectRoute(r'/thanks', handler=views.ThanksHandler, strict_slash=True, name="thanks")),
    (RedirectRoute(r'/cmr/', handler=cmr.indexHandler, strict_slash=True, name="cmr home")),
    (RedirectRoute(r'/cmr/<ref>', handler=cmr.RefHandler, strict_slash=True, name="cmr ref")),
    (webapp2.Route(r'/phn/calc/', handler=phn.CalcHandler, name='PHN BMI Calcs')),
    (webapp2.Route(r'/phn', handler=phn.PHNHandler, name="PHN ZScores")),
    (webapp2.Route(r'/cpet/calc/', handler=exercise.CalcHandler, name='CPET Calcs')),
    (webapp2.Route(r'/cpet', handler=exercise.CPETandler, name="CPET ZScores")),
    (webapp2.Route(r'/calc/echo/<ref>/', handler=echo.CalcHandler )),
    (webapp2.Route(r'/calc/cmr/<ref>/', handler=cmr.CalcHandler )),
    ('/', views.MainHandler),
]

app = webapp2.WSGIApplication(_routes, debug=True, config=myconfig)
app.error_handlers[404] = err.handle_404
app.error_handlers[500] = err.handle_500
