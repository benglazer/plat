# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    long_description = f.read()

setup(
    name='plat',
    version='0.1',
    description='At command interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ben Glazer',
    author_email='ben@benglazer.com',
    url='https://github.com/benglazer/plat',
    license='MIT',
    license_files=['LICENSE'],
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Shells',
        'Topic :: System :: Systems Administration',
    ],
)
