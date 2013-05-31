from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-sdrdltheme',
	version=version,
	description="Design extension for SDRDL",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Eric Busboom',
	author_email='eric@sandiegodata.org',
	url='http://www.sandiegodata.org',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.sdrdltheme'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		'pywordpress'
	],
	entry_points=\
	"""
    [ckan.plugins]
	# Add plugins here, eg
	hello=ckanext.sdrdltheme.hello:HelloWorldPlugin
	sdrdltheme=ckanext.sdrdltheme.plugin:ThemePlugin
	""",
)
