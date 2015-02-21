#!/usr/bin/env python

from setuptools import setup

setup(name='redditstats',
      version='1.0',
      description='Statistics and Analytics for Redit',
      author='Alexaeder Welch',
      author_email='amwelch3@gmail.com',
      install_requires=['praw', 'arrow', 'pandas', 'numpy', 'matplotlib'],
      test_requires=['unittest', 'mock'],
      packages=['redditstats'],
     )
