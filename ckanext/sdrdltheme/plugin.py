# Example Extension
# This extension adds a new template helper function `hello_world` when
# enabled templates can `{{ h.hello_world() }}` to add this html snippet.

import ckan.plugins as p
import ckan.plugins.toolkit as tk
import logging 
import os
import ckanext.sdrdltheme

log = logging.getLogger(__name__)

log.info("Getting started with theme")


def after(instance, action, **params):
    pass



class ThemePlugin(p.SingletonPlugin):

    p.implements(p.ITemplateHelpers)
    p.implements(p.IConfigurer)

    def update_config(self, config):
        log.info("In update_config")
        tk.add_template_directory(config, 'theme/templates')
        tk.add_public_directory(config, 'theme/public')
        tk.add_resource('theme/public', 'ckanext-sdrdltheme')

    @staticmethod
    def hello_world():
        # This is our simple helper function.
        html = '<span>Hello World</span>'
        return p.toolkit.literal(html)

    def get_helpers(self):
        log.info("Returning helpers")
        # This method is defined in the ITemplateHelpers interface and
        # is used to return a dict of named helper functions.
        return {'hello_world': self.hello_world}