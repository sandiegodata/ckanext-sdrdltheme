ckanext-sdrdltheme
==================

Design theme for CKAN


Development Notes. 
==================

Error: AttributeError: 'module' object has no attribute 'css/main.debug.css'
----------------------------------------------------------------------------

http://stackoverflow.com/questions/13480800/ckan-development-install-issue-attributeerror-module-object-has-no-attribute

You need to run the less script from the bin directory in the CKAN source code to build the main.debug.css file. There is some documentation of this but it's not yet integrated with the rest of the CKAN docs (i.e. there's no link to it anywhere, we have a ticket to fix this).

This works on Ubuntu 12.04, you might need to have your virtualenv active when you do this:

sudo apt-get install nodejs npm
npm install less nodewatch
./bin/less # Assuming you're in your ckan dir e.g. `~/pyenv/src/ckan`
Now restart the paster serve development.ini command and it should work.

Generally speaking whenever running CKAN 2.0 for development you should:

Have debug = True in your ini file
Have ./bin/less running in a terminal all the time


