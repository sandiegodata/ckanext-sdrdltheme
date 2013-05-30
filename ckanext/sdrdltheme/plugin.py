# See ckan/ckan/plugins.toolkit.py for a list of the components of the Plugins toolkit, 
# including the template context. 

import ckan.plugins as p
import ckan.plugins.toolkit as tk
import logging 
import os
import ckanext.sdrdltheme
import jinja2

from pylons.i18n import _
from pylons import g, c, config, cache
import sqlalchemy.exc

import ckan.logic as logic
import ckan.lib.maintain as maintain
import ckan.lib.search as search
import ckan.lib.base as base
import ckan.model as model
import ckan.lib.helpers as h

log = logging.getLogger(__name__)

log.info("Getting started with theme")

def after(instance, action, **params):
    pass

class ThemePlugin(p.SingletonPlugin):

    p.implements(p.ITemplateHelpers)
    p.implements(p.IConfigurer)
    p.implements(p.IRoutes, inherit=True)

    def get_packages(self):
        
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}
                   
        data_dict = {
            'q': '*:*',
            'facet.field': g.facets,
            'rows': 4,
            'start': 0,
            'sort': 'views_recent desc',
            'fq': 'capacity:"public"'
        }
        
        query = logic.get_action('package_search')(context, data_dict)
        c.search_facets = query['search_facets']
        c.package_count = query['count']
        c.datasets = query['results']

    def update_config(self, config):
        log.info("In update_config")
        tk.add_template_directory(config, 'theme/templates')
        tk.add_public_directory(config, 'theme/public')
        tk.add_resource('theme/public', 'ckanext-sdrdltheme')
   
    @staticmethod
    def font_size(count):
        """" Return a font size base don a number of views of a package"""
        import math
    
        if count == 0:
            return 100
        else:
            # Range from 100 -> 200% for counts from 1 - 2000
            return 100 + int(math.log(count) * (100/7))
        
        
    @staticmethod
    def log_context():
        import pprint

        log.info("Context: {}".format(type(tk.c)))
        
        for k in dir(tk.c):
            if k.startswith('_'):
                continue
            try:  
                v = getattr(tk.c,k)

                log.info("Context: {}->{}".format(pprint.pformat(k), pprint.pformat(type(v))))
            except Exception as e:
                log.info('Failed for {}: {} '.format(k, str(e)))
            
    @staticmethod
    def hello_world():
        # This is our simple helper function.
        html = '<span>Hello World</span>'

        return p.toolkit.literal(html)

    def get_helpers(self):
        log.info("Returning helpers")
        # This method is defined in the ITemplateHelpers interface and
        # is used to return a dict of named helper functions.
        return {
            'hello_world': self.hello_world,
            'log_context': self.log_context,
            'font_size' : self.font_size
        }
        
    def before_map(self, map):
        log.info("before_map")
        
        map.connect('/',
                    controller='ckanext.sdrdltheme.controllers.home:HomeController',
                    action='index')
        
        
        return map
        
        