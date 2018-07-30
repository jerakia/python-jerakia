import yaml
import os.path
import requests
import json


class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class JerakiaError(Error):
    """Exception raised for errors in the Jerakia lib.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class Jerakia(object):
    """Constructor."""
    def __init__(self,configfile=None):
        if configfile is None:
            self.config = None
        else:
            self.config = self.combined_config(configfile)

    def set_config(self, configfile):
        self.config=self.combined_config(configfile)
    
    def get_config(self):
        return self.config

    """Default coniguration"""
    def config_defaults(self):
        return { 
            'protocol': 'http',
            'host': '127.0.0.1',
            'port': '9843',
            'version': '1',
            'policy': 'default'
        }
        
    """Merge Jerakia coniguration"""
    def merge_dict(self, a, b):
        a = a.copy()
        a.update(b)
        return a

    """Retrieve coniguration"""
    def combined_config(self, configfile):
        defaults = self.config_defaults()

        if os.path.isfile(configfile):
            data = open(configfile, "r")
            defined_config = yaml.load(data)
            combined_config = self.merge_dict(a=defaults,b=defined_config)
            return combined_config
        else:
            raise JerakiaError("Unable to find configuration file %s" % configfile)

    """Lookup endpoint"""
    def lookup_endpoint_url(self, key=''):
        proto = self.config["protocol"]
        host = self.config['host']
        port = self.config['port']
        version = self.config['version']
        url = "%(proto)s://%(host)s:%(port)s/v%(version)s/lookup/%(key)s" % locals() 
        return url

    """Scope definition"""
    def scope(self, variables):
        scope_data = {}
        scope_conf = self.config['scope']
        if not self.config['scope']:
            return {}
        for key, val in scope_conf.iteritems():
            metadata_entry = "metadata_%(key)s" % locals()
            scope_data[metadata_entry] = val
        return scope_data

    """HTTP request header"""    
    def headers(self):
        token = self.config['token']
        if not token:
            raise JerakiaError('No token configured for Jerakia')

        return {
            'X-Authentication': token
        }

    """Lookup method"""
    def lookup(self, key, namespace, policy='default', variables=None):
        endpoint_url = self.lookup_endpoint_url(key=key)
        namespace_str = '/'.join(namespace)
        scope = self.scope(variables)
        options = { 
            'namespace': namespace_str,
            'policy': policy,
        }

        params = self.merge_dict(a=scope,b=options)
        headers = self.headers()

        response = requests.get(endpoint_url, params=params, headers=headers)
        if response.status_code == requests.codes.ok:
          return json.load(response.json())
        else:
          raise JerakiaError("Bad HTTP response")
