import credstash
import mock
import pytest

from secretstash import ItemNotFound, SecretStash


def test_local(fs):
    fs.create_file('/secrets.toml', contents='[a.b]\nc = "secret"')
    stash = SecretStash('non-region', '/secrets.toml')
    assert stash.get_secret('a.b.c', {}) == 'secret'


@mock.patch('credstash.getSecret')
def test_credstash_fallback(getSecret_mock):
    getSecret_mock.side_effect = lambda *args, **kwargs: 'nope'
    stash = SecretStash('non-region', '/secrets.toml')
    assert stash.get_secret('a.b.c', {}) == 'nope'


@mock.patch('credstash.getSecret')
def test_no_local_key(getSecret_mock, fs):
    getSecret_mock.side_effect = lambda *args, **kwargs: 'nope'
    fs.create_file('/secrets.toml', contents='')
    stash = SecretStash('non-region', '/secrets.toml')
    assert stash.get_secret('a.b.c', {}) == 'nope'


@mock.patch('credstash.getSecret')
def test_credstash_passthrough(getSecret_mock):
    def getSecret(name, region, context):
        return '{}-{}-{}'.format(name, region, context)

    getSecret_mock.side_effect = getSecret
    stash = SecretStash('coolregion', '/secrets.toml')
    assert stash.get_secret('a.b.c', {'context': 'foo'}) \
        == "a.b.c-coolregion-{'context': 'foo'}"


@mock.patch('credstash.getSecret')
def test_item_not_found(getSecret_mock):
    getSecret_mock.side_effect = credstash.ItemNotFound
    stash = SecretStash('coolregion', '/secrets.toml')
    with pytest.raises(ItemNotFound):
        stash.get_secret('a.b.c', {})
