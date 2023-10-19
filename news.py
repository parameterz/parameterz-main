# Copyright (C) 2011 by Matt Woodfield
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import re
import cgi
import yaml
import webapp2
import config
import views
from google.appengine.api import memcache
import logging

class Article:
  def __init__(self, article_id):
    self.id       = re.sub('.md', '', article_id)
    self.id       = re.sub('.txt', '', article_id)
    self.raw      = self.load()

    if self.raw is not None:
      self.raw      = self.raw.split("---", 1)
      self.url      = config.site_url+re.sub('-', '/', self.id, 3)
      self.meta     = yaml.load(self.raw[0])
      self.summary  = (self.raw[1].split('!!!', 1)[0])
      self.body     = (self.raw[1].split('!!!', 1)[1])
    
  def load(self):
    article = memcache.get(self.id, 'article_')
    if article is None:
      try:
        static_article_path = path(config.articles_dir+self.id+config.article_file_type)
        article = file(static_article_path, 'rb').read()
        memcache.set(self.id, article, config.cache_time, 0, 'article_')
      except IOError: return
    return article

class Articles:
  def all(self):
    archives = Archives().all("", config.articles_per_page)
    articles = []
    for archive in archives:      
      article = Article(archive['name'])
      if article.raw is not None:
        articles.append(article)
    return articles

class Archives:
  def all(self, filter="", limit=25, offset=0):
    index_from  = (limit*offset) 
    index_to    = ((limit*offset)+limit)
    archives = memcache.get('archives_'+filter+"_"+str(index_from)+"_"+str(index_to))
    if archives == None:
      archives    = []
      article_dir = path(config.articles_dir)
      for root, dirs, files in os.walk(article_dir):
        count = 0
        for name in files:
          if filter in name and name.index('.') > 0:
            if count >= index_from and count < index_to:
              name    = re.sub('.md', '', name)
              name    = re.sub('.txt', '', name)
              url     = '/'+re.sub('-', '/', name, 3)
              archive = {
                'name' : name,
                'url'  : url
              }
              archives.append(archive)
            count += 1
      archives = sorted(archives, key=lambda archive:archive['name'])[::-1]
      memcache.set('archives_'+filter+"_"+str(index_from)+"_"+str(index_to), archives, config.cache_time)
    return archives

class Index(views.BaseHandler):
  def get(self):
    articles = Articles().all()
    self.render_template('news/index.html', articles = articles, page ={'title': 'News', 'description': 'news home page'})

class ViewArticle(views.BaseHandler):
  def get(self, year, month, day, title):
    article_id    = cgi.escape(year)+'-'+cgi.escape(month)+'-'+cgi.escape(day)+'-'+cgi.escape(title)
    article       = Article(article_id)
    if article.raw is not None:
      self.render_template('news/article.html',
                           article = article,
                           page = {'title': 'News | ' + article.meta['title'],
                                   'description': article.meta['description']})
    else:
      webapp2.abort(404)

class Changelog(views.BaseHandler):
  def get(self):
      self.render_template('news/changelog.html',
                           page = {'title': 'Changelog',
                                   'description': 'parameterz changelog'})

class ViewArchives(views.BaseHandler):
  #not working ... yet
  def get(self, year=None, month=None, day=None):
    if year == None:
      archives = Archives().all()
    else:
      filter = cgi.escape(year)
      if month is not None: 
        filter += '-'+cgi.escape(month)
        if day is not None: 
          filter += '-'+cgi.escape(day)
      archives = Archives().all(filter)
    self.render_template('pages/archives.html', 
                        archives = archives,
                        year = year,
                        month = month,
                        day = day,
                        page = {'title': 'Archives', 'description': ''})

class PageHandler(views.BaseHandler):
  def get(self, page):
    page = cgi.escape(page.replace('/', ''))
    try: 
        return self.render_template('pages/' + page + '.html', page = {'title': page, 'description': 'none'})
    except:
        webapp2.abort(404)
    
def path(path):
  return os.path.join(os.path.dirname(__file__), path)

class Admin(webapp2.RequestHandler):
  def get(self, action):
    if action == "flush":
      self.response.write('Flushing...')
      memcache.flush_all()
      self.redirect('/')
    else:
      webapp2.abort(404)
  
  
