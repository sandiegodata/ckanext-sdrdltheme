import os
import re
import urllib
import uuid
from datetime import datetime
from cgi import FieldStorage

from ofs import get_impl
from pylons import request, response
from pylons.controllers.util import abort, redirect_to
from pylons import config
from paste.fileapp import FileApp
from paste.deploy.converters import asbool

from ckan.lib.base import BaseController, c, request, render, config, h, abort
from ckan.lib.jsonp import jsonpify
import ckan.model as model
import ckan.new_authz as new_authz
import logging 

import ckan.controllers.storage
from  ckan.controllers.storage import authorize

log = logging.getLogger(__name__)

BUCKET = config.get('ckan.storage.bucket', 'default')
key_prefix = config.get('ckan.storage.key_prefix', 'file/')

def get_key(ofs, label):

    bucket = BUCKET
    
    try:
        b = ofs._require_bucket(bucket)
    except:
        log.info("Exception")
        abort(409)

    if not label.startswith("/"):
        label = "/" + label

    k = ofs._get_key(b, label)    
    
    return k

class StorageAPIController(ckan.controllers.storage.StorageAPIController):
    
    @jsonpify
    def auth_form(self, label):
        '''Provide fields for a form upload to storage including
        authentication.

        :param label: label.
        :return: json-encoded dictionary with action parameter and fields list.
        '''
        bucket = BUCKET
        if request.POST:
            try:
                data = fix_stupid_pylons_encoding(request.body)
                headers = json.loads(data)
            except Exception, e:
                from traceback import print_exc
                msg = StringIO()
                print_exc(msg)
                log.error(msg.seek(0).read())
                abort(400)
        else:
            headers = dict(request.params)

        method = 'POST'
        authorize(method, bucket, label, c.userobj, self.ofs)
        data = self._get_form_data(label)
        
        #log.info("Request auth: "+str(data))

        return data

    @jsonpify
    def get_metadata(self, label):
        log.info("child")
        bucket = BUCKET
        storage_backend = config['ofs.impl']
        if storage_backend in ['google', 's3']:
            if not label.startswith("/"):
                label = "/" + label
            url = "https://%s%s" % (
                self.ofs.conn.calling_format.build_host(
                    self.ofs.conn.server_name(), bucket), label)

            k = get_key(self.ofs, label)
                    
            url = k.generate_url(60*60*24*365*10, force_http=True)
            log.info("get_metadata. url={}".format(url))
            
        else:
            url = h.url_for('storage_file',
                            label=label,
                            qualified=False
                            )
            if url.startswith('/'):
                url = config.get('ckan.site_url','').rstrip('/') + url

        if not self.ofs.exists(bucket, label):
            abort(404)
        metadata = self.ofs.get_metadata(bucket, label)
        metadata["_location"] = url
        return metadata

    # Override the parent to remove the make_public() call. 
    def set_metadata(self, label):
        log.info("In parent set_metadata")
        bucket = BUCKET
        if not label.startswith("/"):
            label = "/" + label

        try:
            data = fix_stupid_pylons_encoding(request.body)
            if data:
                metadata = json.loads(data)
            else:
                metadata = {}
        except:
            abort(400)

        try:
            b = self.ofs._require_bucket(bucket)
        except:
            abort(409)

        k = self.ofs._get_key(b, label)
        if k is None:
            k = b.new_key(label)
            metadata = metadata.copy()
            metadata["_creation_time"] = str(datetime.utcnow())
            self.ofs._update_key_metadata(k, metadata)
            k.set_contents_from_file(StringIO(''))
        elif request.method == "PUT":
            old = self.ofs.get_metadata(bucket, label)
            to_delete = []
            for ok in old.keys():
                if ok not in metadata:
                    to_delete.append(ok)
            if to_delete:
                self.ofs.del_metadata_keys(bucket, label, to_delete)
            self.ofs.update_metadata(bucket, label, metadata)
        else:
            self.ofs.update_metadata(bucket, label, metadata)

        k.close()

class StorageController(ckan.controllers.storage.StorageController):
    
    def success_empty(self, label=None):
        # very simple method that just returns 200 OK
        label = request.GET['label']
        log.info("success_empty. label={}".format(label))

        #log.info('URL: '+str(k.generate_url(60, force_http=True)))
        #log.info('URL: '+str(k.generate_url(60*60*24*365*10, force_http=True)))
        
        k = get_key(self.ofs, label)
        k.set_acl('private')
        
        return ''