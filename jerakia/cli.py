import sys
import os
import collections
import errno
import subprocess
import six
import click
from os import walk
from .client import Client,ClientError
from pkg_resources import iter_entry_points
from click_plugins import with_plugins
from distutils import dir_util # https://github.com/PyCQA/pylint/issues/73; pylint: disable=no-name-in-module

sys.path.insert(0, os.getcwd())

class InvalidDataFormat(Exception):
    """Invalid data exception"""
    pass

class InvalidInputData(Exception):
    """Invalid input data exception"""
    pass

class MalformedYAML(InvalidInputData):
    """Invalid YAML data exception"""
    pass

def get_format(fmt):
    """Returns a data loading function"""
    try:
        return FORMATS[fmt]()
    except ImportError:
        raise InvalidDataFormat(fmt)

def _load_yaml():
    import yaml
    return yaml.load, yaml.YAMLError, MalformedYAML

def merge_dict(a, b):
    """Merge Jerakia coniguration"""
    a = a.copy()
    a.update(b)
    return a

FORMATS = {
    'yaml': _load_yaml,
    'yml': _load_yaml,
}


@with_plugins(iter_entry_points('jerakia.plugins'))
@click.group()
def main():
    """jerakia is a tool to perform hierarchical data lookups."""

@main.command()
@click.argument('namespace')
@click.argument('key')
@click.option('-T','--token')
@click.option('-P','--port')
@click.option('-t','--type')
@click.option('-H','--host')
@click.option('--protocol', default='http')
@click.option('-p','--policy')
@click.option('-m', '--metadata')
@click.option('-i', '--configfile', type=click.Path(), default='$HOME/.jerakia/jerakia.yaml')
def lookup(namespace,key,token,port,type,host,protocol,policy,metadata,configfile):
    if os.path.exists(configfile):
        with open(configfile, "r") as filename:
            config = yaml.load(filename)
    else:
        config  = dict()
    options_config = dict(token=token,port=port,host=host,version=1,protocol=protocol)
    combined_config = merge_dict(a=config,b=options_config)         
    jerakiaobj = Client(token=token)
    ns = []
    ret = []
    ns.append(str(namespace))
    response = jerakiaobj.lookup(key=str(key), namespace=ns, metadata_dict=metadata, content_type='json')
    ret.append(response['payload'])

    if len(ret) == 1:
        try:
            print ("Result outputs", response['payload'].encode('ascii', 'ignore'))
        except Exception as detail:
            print 'The Jerakia lookup resulted in an empty response:', detail
    else:
        try:
            [x.encode('ascii', 'ignore') for x in ret]
            print ("Result outputs ", ret)
        except Exception as detail:
            print 'The Jerakia lookup resulted in an empty response:', detail

if __name__ == '__main__':
    greet(auto_envvar_prefix='JERAKIA')