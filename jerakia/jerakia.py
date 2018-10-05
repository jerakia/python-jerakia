import yaml
import os.path
import requests
import json
import msgpack
import pprint

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
    def __init__(self, **kwargs):
        self.config = self.default_config()
        for attr in ('protocol', 'host', 'port', 'version'):
            if kwargs.get(attr) is not None:
                self.config[attr] = kwargs.get(attr)
        self._content_type = dict(json = 'application/json',
                msgpack = 'application/x-msgpack')
        self.session = requests.Session()


    @classmethod
    def fromfile(cls, configfile):
        """Initialize jerakia object with a config file"""
        if os.path.isfile(configfile):
            with open(configfile, "r") as f:
                config = yaml.load(f)
        else:
            raise JerakiaError("Unable to find configuration file {}".format(configfile))
        return cls(**config)


    def default_config(self):
        """Set the jerakia default values"""
        return dict(
                protocol = 'http', 
                host = 'localhost',
                port = 9843,
                version = 1 
                )
    

    def get_config(self):
        """Return the jerakia config dict"""
        return self.config


    def lookup(self, **kwargs):
        url = '{}://{}:{}/v{}/lookup'.format(self.config['protocol'],
                self.config['host'], self.config['port'],
                self.config['version'])     

        headers = dict()
        headers['content-type'] = self._content_type['msgpack']
        params = dict()
        params['policy'] = 'default'
        params['scope'] = 'metadata'
        
        for attr in ('key', 'namespace', 'policy', 'lookup_type', 'merge', 'scope',
                'scope_dict', 'metadata_dict', 'token', 'content_type'):
            if kwargs.get(attr) is not None:
                if attr == 'metadata_dict':
                    for key, val in kwargs.get(attr).items():
                        params['metadata_{}'.format(key)] = val
                elif attr == 'scope_dict':
                    for key, val in kwargs.get(attr).items():
                        params['scope_{}'.key] = val
                elif attr == 'key':
                    url = "{}/{}".format(url, kwargs.get(attr))
                elif attr == 'token':
                    headers['x-authentication'] = kwargs.get(attr)
                elif attr == 'content_type':
                    headers['content-type'] = self._content_type[kwargs.get(attr)]
                else:
                    params[attr] = kwargs.get(attr)
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise JerakiaError("Bad HTTP response: {}".format(err))
        return self._unpack_response(response)


    def _unpack_response(self, response):
        if response.headers['content-type'] == self._content_type['json']:
            return response.json()
        elif response.headers['content-type'] == self._content_type['msgpack']:
            return msgpack.unpackb(response.content)
        else:
            raise JerakiaError("Unkown content-type recieved from jerakia server: {}".format(response.headers['content-type']))
