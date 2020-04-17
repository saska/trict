
from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))

version = '0.1.4'

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'trict',
  packages = ['trict'],
  version = version,
  license='MIT',
  description = 'UserDict subclass with extra stuff',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Saska Karsi',
  author_email = 'saska.karsi@gmail.com',
  url = 'https://github.com/saskakarsi/trict',
  keywords = ['mapping', 'map', 'dictionary', 'recursive', 'dict'],
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)