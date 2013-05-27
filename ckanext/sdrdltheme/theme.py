# Example Extension
# This extension adds a new template helper function `hello_world` when
# enabled templates can `{{ h.hello_world() }}` to add this html snippet.

import ckan.plugins as p
import logging 
import os
import ckanext.sdrdltheme

log = logging.getLogger(__name__)

log.info("Getting started with theme")


def after(instance, action, **params):
    log.info("AFTER")

def configure_template_directory(config, relative_path):
    configure_served_directory(config, relative_path, 'extra_template_paths')

def configure_public_directory(config, relative_path):
    configure_served_directory(config, relative_path, 'extra_public_paths')

def configure_served_directory(config, relative_path, config_var):
    'Configure serving of public/template directories.'
    assert config_var in ('extra_template_paths', 'extra_public_paths')
    this_dir = os.path.dirname(ckanext.sdrdltheme.__file__)
    absolute_path = os.path.join(this_dir, relative_path)
    if absolute_path not in config.get(config_var, ''):
        if config.get(config_var):
            config[config_var] = absolute_path + ',' + config[config_var]
        else:
            config[config_var] = absolute_path


class ThemePlugin(p.SingletonPlugin):

    p.implements(p.ITemplateHelpers)
    p.implements(p.IConfigurer)

    def update_config(self, config):
        log.info("In update_config")
        configure_template_directory(config, 'theme/templates')
        configure_public_directory(config, 'theme/public')


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