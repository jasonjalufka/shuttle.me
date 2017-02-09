#!/usr/bin/env python
from setuptools import setup, find_packages

setup  (
    name        = 'doublemap',
    version     = '0.0.1',
    description = 'An API client for DoubleMap.',
    author = 'Travis Cunningham',
    author_email = 'travcunn@umail.iu.edu',
    url = 'https://github.com/travcunn/doublemap',
    license = 'MIT',
    packages  =  find_packages('src'),
    package_dir = {'' : 'src'},
    entry_points = {
        'console_scripts': [
            'doublemap = doublemap.__init__:main',
        ],
    },
)
