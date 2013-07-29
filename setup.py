#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptest import test


tests_require = [
    'django-nose'
]

install_requires = [
    'Django>=1.4,<1.6',
    'richenum>=0.1.0,<1.0'
]


setup(
    name='django-richenum',
    version='0.1.0',
    description='Django Enum library for python.',
    long_description=open('README.md').read(),
    classifiers=[],
    keywords='python django enum richenum',
    url='https://github.com/hearsaycorp/django-richenum',
    author='Hearsay Social',
    author_email='opensource@hearsaysocial.com',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='tests',
    zip_safe=False
)
