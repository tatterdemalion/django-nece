# -*- coding: utf-8 -*-
from setuptools import setup

description = "A content translation framework using Postgresql's " +\
    "jsonb field in the background",

version = '0.4'
url = 'https://github.com/tatterdemalion/django-nece'
download_url = '/'.join([url, 'tarball', version])

setup(
    name='nece',
    version=version,
    description=description,
    long_description=description,
    author='Can Mustafa Özdemir',
    author_email='canmustafaozdemir@gmail.com',
    url=url,
    download_url=download_url,
    keywords=['translations', 'i18n', 'language', 'multilingual'],
    packages=['nece', 'nece.fields', 'nece.fields.pgjson',
              'nece.fields.pgjson.forms'],
    install_requires=[
        'Django>=1.8',
    ],
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Database",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Text Processing :: Linguistic",
    ],
)
