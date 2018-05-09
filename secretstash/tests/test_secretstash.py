import pytest

from secretstash import SecretStash


def test_local(fs):
    fs.create_file('/secrets.toml', contents='[a.b]\nc = "secret"')
    stash = SecretStash('non-region', '/secrets.toml')
    assert stash.get_secret('a.b.c', {}) == 'secret'
