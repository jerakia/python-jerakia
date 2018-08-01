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
    def __init__(self,configfile):
        if configfile is None:
            self.config = None
        else:
            self.config = self.combined_config(configfile)

    def set_config(self, configfile):
        self.config=self.combined_config(configfile)
    
    def get_config(self):
        return self.config

    def config_defaults(self):
        """Default coniguration"""
        return { 
            'protocol': 'http',
            'host': '127.0.0.1',
            'port': '9843',
            'version': '1',
            'policy': 'default'
        }
        
    def merge_dict(self, a, b):
        """Merge Jerakia coniguration"""
        a = a.copy()
        a.update(b)
        return a

    def combined_config(self, configfile):
        """Retrieve coniguration"""
        defaults = self.config_defaults()
        if os.path.isfile(configfile):
            data = open(configfile, "r")
            defined_config = yaml.load(data)
            combined_config = self.merge_dict(a=defaults,b=defined_config)
            return combined_config
        else:
            raise JerakiaError("Unable to find configuration file %s" % configfile)

    def lookup_endpoint_url(self, key=''):
        """Lookup endpoint"""
        proto = self.config["protocol"]
        host = self.config['host']
        port = self.config['port']
        version = self.config['version']
        url = "%(proto)s://%(host)s:%(port)s/v%(version)s/lookup/%(key)s" % locals() 
        return url

    def scope(self, variables):
        """Scope definition"""
        scope_data = {}
        scope_conf = self.config['scope']
        if not self.config['scope']:
            return {}
        for key, val in scope_conf.iteritems():
            metadata_entry = "metadata_%(key)s" % locals()
            scope_data[metadata_entry] = val
        return scope_data
    
    def headers(self):
        """HTTP request header"""
        token = self.config['token']
        if not token:
            raise JerakiaError('No token configured for Jerakia')

        return {
            'X-Authentication': token
        }

    def lookup(self, key, namespace, policy='default', variables=None):
        """Lookup method"""
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
          return json.loads(response.text)
        else:
          raise JerakiaError("Bad HTTP response")
