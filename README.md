# secretstash

This is a library that abstracts over two different secrets backends:

- [credstash](https://pypi.org/project/credstash/)
- an unencrypted TOML file.

The idea is that, while in real deployments you may want to use credstash,
during local development you would like to be able to get by without connecting
to credstash.
