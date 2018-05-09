import os
from setuptools import setup, find_packages

requirements = ['credstash', 'toml']

setup(
    name='secretstash',
    version='0.1.0',
    description='Wrapper around credstash + local file',
    author='Juice Developers',
    author_email='chris@juice.com',
    packages=find_packages(),
    install_requires=requirements,
)
