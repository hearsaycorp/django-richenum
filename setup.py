#!/usr/bin/env python

# W/o multiprocessing, nosetests can't exit cleanly.
# (See http://bugs.python.org/issue15881#msg170215)
import multiprocessing  # noqa
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


tests_require = (
    'django-nose',
)


install_requires = (
    'Django>=1.4,<1.7',
    'richenum',
)


class DjangoTest(TestCommand):
    DIRNAME = os.path.dirname(__file__)
    APPS = ('tests',)

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from django.conf import settings
        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(self.DIRNAME, 'database.db')}},
            CACHES={
                'default': {
                    'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}},
            INSTALLED_APPS=('django_nose',) + self.APPS)

        from django_nose import NoseTestSuiteRunner
        runner = NoseTestSuiteRunner(failfast=False, interactive=False)
        sys.exit(runner.run_tests(self.APPS))


setup(
    name='django-richenum',
    version='1.2.1',
    description='Django Enum library for python.',
    long_description=(
        open('README.rst').read() + '\n\n' +
        open('CHANGELOG.rst').read() + '\n\n' +
        open('AUTHORS.rst').read()),
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
    cmdclass={'test': DjangoTest},
)
