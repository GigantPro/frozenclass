#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: GigantPro
:license: The GPLv3 License (GPLv3), see LICENSE file
:copyright: (c) 2023 Xiver organization
"""

version = '0.0.2a'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pysavedata',
    version=version,

    author='GigantPro',
    author_email='gigantpro2000@gmail.ru',

    description=(
        'Python module for convenient storage of classes in files.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/GigantPro/pysavedata',
    download_url='https://github.com/Peopl3s/club-house-api/archive/main.zip',

    license='The GPLv3 License (GPLv3), see LICENSE file',

    packages=['pysavedata'],
    install_requires=[],

    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)