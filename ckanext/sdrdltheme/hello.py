# Example Extension
# This extension adds a new template helper function `hello_world` when
# enabled templates can `{{ h.hello_world() }}` to add this html snippet.

import ckan.plugins as p

class HelloWorldPlugin(p.SingletonPlugin):

    p.implements(p.ITemplateHelpers)

    @staticmethod
    def hello_world():
        # This is our simple helper function.
        html = '<span>Hello World</span>'
        return p.toolkit.literal(html)

    def get_helpers(self):
        # This method is defined in the ITemplateHelpers interface and
        # is used to return a dict of named helper functions.
        return {'themer': self.hello_world}