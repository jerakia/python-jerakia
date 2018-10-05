"""
lib for performing Jerakia lookups with Ansible
"""

import sys
import os
from .jerakia import Jerakia,JerakiaError
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase

class JerakiaAnsible(Jerakia):
    def __init__(self,configfile):
        Jerakia.__init__(self,configfile)
    def dot_to_dictval(self, dic, key):
      key_arr = key.split('.')
      this_key = key_arr.pop(0)

      if not this_key in dic:
        raise AnsibleError("Cannot find key %s " % key)

      if len(key_arr) == 0:
        return dic[this_key]

      return self.dot_to_dictval(dic[this_key], '.'.join(key_arr))


    def scope(self, variables):
        scope_data = {}
        scope_conf = self.config['scope']
        if not self.config['scope']:
            return {}
        for key, val in scope_conf.iteritems():
            metadata_entry = "metadata_%(key)s" % locals()
            scope_value = self.dot_to_dictval(variables, val)
            scope_data[metadata_entry] = scope_value
        return scope_data

# Entry point for Ansible starts here with the LookupModule class
class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

         jerakia = JerakiaAnsible(self)
         ret = []

         for term in terms:
             lookuppath=term.split('/')
             key = lookuppath.pop()
             namespace = lookuppath

             if not namespace:
                 raise AnsibleError("No namespace given for lookup of key %s" % key)

             response = jerakia.lookup(key=key, namespace=namespace, variables=variables)
             ret.append(response['payload'])

         return ret