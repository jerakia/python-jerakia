import os.path
import sys
import requests
import msgpack
import yaml


def merge_dicts(*dicts):
    result = {}
    for dictionary in dicts:
        result.update(dictionary)
    return result


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
    def __init__(self, token, protocol='http', host='localhost', port=9843,
                 version=1):
        self.config = dict(token=token, protocol=protocol, host=host,
                           port=port, version=version)
        self._content_type = dict(json='application/json',
                                  msgpack='application/x-msgpack')
        self.session = requests.Session()

    @classmethod
    def fromfile(cls, configfile):
        """Initialize jerakia object with a config file"""
        if os.path.isfile(configfile):
            with open(configfile, "r") as filename:
                config = yaml.load(filename)
        else:
            raise JerakiaError("""Unable to find configuration file
                    {}""".format(configfile))
        return cls(**config)

    def get_config(self):
        """Return the jerakia config dict"""
        return self.config

    def lookup(self, namespace, key=None, merge=None, lookup_type=None,
               content_type='msgpack', policy=None, scope=None,
               scope_dict=None, metadata_dict=None):

        def dict_attr(dictionary, prefix):
            target = dict()
            for key, val in dictionary.items():
                target['{}_{}'.format(prefix, key)] = val
            return target

        params = {k: v for k, v in (('namespace', namespace), ('merge', merge),
                                    ('policy', policy), ('scope', scope),
                                    ('lookup_type', lookup_type))
                  if v is not None}
        headers = {k: v for k, v in (('x-authentication',
                                      self.config['token']),
                                     ('content-type',
                                      self._content_type[content_type]))
                   if v is not None}

        if metadata_dict is not None:
            params = merge_dicts(params, dict_attr(metadata_dict, 'metadata'))
        if scope_dict is not None:
            params = merge_dicts(params, dict_attr(scope_dict, 'scope'))

        url = '{}://{}:{}/v{}/lookup'.format(
            self.config['protocol'],
            self.config['host'], self.config['port'],
            self.config['version'])
        if key is not None:
            url = "{}/{}".format(url, key)

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("Bad HTTP response: {}".format(err))
            result = response.json()
            print("Jerakia lookup {}: '{}'.".format(result['status'],
                  result['message']))
            sys.exit(1)
        return self._unpack_response(response)

    def _unpack_response(self, response):
        if response.headers['content-type'] == self._content_type['json']:
            return response.json()
        elif response.headers['content-type'] == self._content_type['msgpack']:
            return msgpack.unpackb(response.content)
        else:
            raise JerakiaError("""Unkown content-type recieved from jerakia
            server: {}""".format(response.headers['content-type']))
