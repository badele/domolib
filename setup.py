#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

PYPI_MD_FILTERS = (
    # Replace code-blocks
    (r'\.\.\s? code-block::\s*(\w|\+)+', '::'),
    # Replace image
    (r'\.\.\s? image::.*', ''),
    # Remove travis ci badge
    (r'.*travis-ci\.org/.*', ''),
    # Remove pypip.in badges
    (r'.*pypip\.in/.*', ''),
    (r'.*crate\.io/.*', ''),
    (r'.*coveralls\.io/.*', ''),
)


def md(filename):
    '''
Load rst file and sanitize it for PyPI.
Remove unsupported github tags:
- code-block directive
- travis ci build badge
'''
    content = open(filename).read()
    for regex, replacement in PYPI_MD_FILTERS:
        content = re.sub(regex, replacement, content)
    return content


def required(filename):
    with open(filename) as f:
        all_packages = f.read().splitlines()

    packages = []
    links = []
    for line in all_packages:
        match = re.search(r'.*(git\+git.*)', line)
        if match:
            links.append(match.group(1))
        else:
            packages.append(line)

    return {'packages': packages, 'links': links}


setup(
    name="domolib",
    version="0.0.1",
    description="domolib",
    long_description=md('README.md') + md('CHANGELOG.txt'),
    author="Bruno Adelé",
    author_email="bruno@adele.im",
    url="https://github.com/badele/domolib",
    license="GPL",
    install_requires=required('requirements/base.txt')['packages'],
    dependency_links=required('requirements/base.txt')['links'],
    setup_requires=[],
    tests_require=[
        'pep8',
        'coveralls'
    ],
    test_suite='tests',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=[],
    entry_points={
        'console_scripts': [
            'domolib = domolib.cmd:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python',
    ],
)
