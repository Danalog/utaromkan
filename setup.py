#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for utaromkan."""

from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='utaromkan',
    version=version,
    description="kana <-> romaji conversion for utau",
    long_description=open('README.rst').read(),
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: Japanese",
        "License :: GNU General Public License (GPL)",
    ],
    keywords='hiragana katakana kana romaji japanese utau \xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e',
    author='tart',
    author_email='conemusicproductions@gmail.com',
    url='http://github.com/Danalog/utaromkan',
    license='GPL',
    py_modules = ['utaromkan'],
    #packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite="tests",
    install_requires=[
      # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
