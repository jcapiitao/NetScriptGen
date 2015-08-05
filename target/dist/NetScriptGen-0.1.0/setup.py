#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'NetScriptGen',
          version = '0.1.0',
          description = '''Generate script for network equipments with data stored into an Excel workbook and a template''',
          long_description = '''''',
          author = "Joel Capitao",
          author_email = "joel.capitao93@gmail.com",
          license = '',
          url = '',
          scripts = [],
          packages = ['equipment', 'function', 'process', 'utils', 'equipment.cisco', 'equipment.feature'],
          py_modules = ['__init__', '__main__'],
          classifiers = ['Development Status :: 3 - Alpha', 'Programming Language :: Python'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          
          
          zip_safe=True
    )
