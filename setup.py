#!/usr/bin/env python

from distutils.core import setup

setup(name='pulse-sms-api',
      version='1.0',
      description='A unofficial API for pulse-sms in python',
      author='Per-Arne Andersen',
      author_email='per@sysx.no',
      url='https://github.com/perara-libs/py-pulse-sms-api',
      packages=['pulsesms'],
      install_requires=[
            'python-dotenv>=0.17.0',
            'loguru>=0.5.3',
            'requests>=2.25.1',
            'pycryptodome'
      ])
