#!/usr/bin/env python

from setuptools import setup

setup(name='redditstats',
      version='1.0',
      description='Statistics and Analytics for Redit',
      author='Alexander Welch',
      author_email='amwelch3@gmail.com',
      install_requires=['praw'],
      test_requires=['unittest', 'mock'],
      packages=['redditstats'],
     )
