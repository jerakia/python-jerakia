"""
lib for rendering jinja templates using Jerakia lookups
"""

import sys
import os
from jinja2 import Environment, FileSystemLoader, Template
from .client import Client,ClientError
from jinja2.ext import Extension

jerakia = None
metadata = None

def render(template_path, jerakia_instance, metadata_dict, data, extensions=None, strict=False):
    """Renders a jinja2 template using data looked up via Jerakia"""

    global jerakia
    jerakia = jerakia_instance
    global metadata
    metadata = metadata_dict

    if extensions is None:
        extensions = []
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(template_path)),
        extensions=extensions,
        keep_trailing_newline=True,
    )
    if strict:
        from jinja2 import StrictUndefined
        env.undefined = StrictUndefined

    env.globals['environ'] = os.environ.get
    env.globals['retrieveJerakia'] = retrieveJerakia

    output = env.get_template(os.path.basename(template_path)).render(data)
    return output.encode('utf-8')

def retrieveJerakia(item):
    """Retrieves the result from the Jerakia lookup"""

    global jerakia
    global metadata
    
    lookuppath =item.split('/')
    key = lookuppath.pop()
    namespace = lookuppath
    ret = []
    response = jerakia.lookup(key=key, namespace=namespace, metadata_dict=metadata, content_type='json')
    ret.append(response['payload'])

    if len(ret) == 1:
        try:
            return response['payload'].encode('ascii', 'ignore')
        except Exception as detail:
            print('The Jerakia lookup resulted in an empty response:', detail)
    else:
        try:
            [x.encode('ascii', 'ignore') for x in ret]
            return ret
        except Exception as detail:
            print('The Jerakia lookup resulted in an empty response:', detail)
