import sys
import os
from .client import Client,ClientError
from pkg_resources import iter_entry_points
import click
from click_plugins import with_plugins

sys.path.insert(0, os.getcwd())

@with_plugins(iter_entry_points('jerakia.plugins'))
@click.group()
def main():
    """jerakia is a tool to perform hierarchical data lookups."""

@main.command()
@click.argument('namespace')
@click.argument('key')
@click.argument('token')
@click.argument('metadata', required=False)
def lookup(namespace,key,token,metadata):
    """perform a lookup using Jerakia"""
    jerakiaobj = Client(token=token)
    ns = []
    ret = []
    ns.append(str(namespace))
    response = jerakiaobj.lookup(key=str(key), namespace=ns, metadata_dict=metadata,content_type='json')
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