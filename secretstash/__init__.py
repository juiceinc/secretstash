"""See SecretStash."""

import toml
from credstash import getSecret

__all__ = ['SecretStash']


def dotted_get(obj, name):
    """
    Get a value from a nested dictionary given a dotted name.

    Given a nested dictionary like `{'a': {'b': 'c'}}` and a string "a.b",
    return "c".
    """
    parts = name.split('.')
    cur = obj
    for part in parts:
        cur = cur.get(part, None)
        if cur is None:
            return
    return cur


class SecretStash(object):
    """A wrapper for credstash and a local file."""

    def __init__(self, region, local_filename):
        """Construct with an AWS region and a local filename."""
        self.region = region
        self.local_filename = local_filename

    def get_local(self, name):
        """Get a secret directly from the local file."""
        try:
            with open(self.local_filename) as f:
                data = toml.loads(f.read())
                return dotted_get(data, name)
        except IOError:
            pass

    def get_secret(self, name, context):
        """
        Get a secret.

        First tries to load a secret from the local file, then falls back
        to credstash. The context is not considered when looking secrets up
        in the local file.
        """
        secret = self.get_local(name)
        if secret is None:
            return getSecret(name, region=self.region, context=context)
        else:
            return secret
