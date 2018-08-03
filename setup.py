# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='plat',
    version='0.0.1',
    description='At command interface',
    long_description=readme,
    author='Ben Glazer',
    author_email='ben@benglazer.com',
    url='https://github.com/benglazer/plat',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
