"""
See get_secret
"""

import toml
from credstash import getSecret

__all__ = ['get_secret']


def dotted_get(obj, name):
    parts = name.split('.')
    cur = obj
    for part in parts:
        cur = cur.get(part, None)
        if cur is None:
            return
    return cur


class SecretStash(object):
    def __init__(self, region, local_filename):
        self.region = region
        self.local_filename = local_filename

    def get_local(self, name):
        try:
            with open(self.local_filename) as f:
                data = toml.loads(f.read())
                return dotted_get(data, name)
        except IOError:
            pass

    def get_secret(self, name, context):
        secret = self.get_local(name)
        if secret is None:
            return getSecret(name, region=self.region, context=context)
        else:
            return secret
