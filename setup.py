#!/usr/bin/env python
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


tests_require = (
    'pytest<5.0',
    'pytest-django',
)


install_requires = (
    'Django>=1.11,<2.2',
    'richenum',
    'six',
)


class DjangoTest(TestCommand):
    DIRNAME = os.path.dirname(__file__)
    APPS = ('tests',)

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        from django.conf import settings
        import django

        db_engine = os.environ.get('DJANGO_DB_ENGINE', 'sqlite')
        db_user = os.environ.get('DJANGO_DB_USER')
        if db_engine == 'mysql':
            db_settings = {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'testdb',
                'USER': db_user or 'travis',
            }
        elif db_engine == 'postgres':
            db_settings = {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'testdb',
                'USER': db_user or 'postgres',
            }
        elif db_engine == 'sqlite':
            db_settings = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(self.DIRNAME, 'database.db'),
            }
        else:
            raise ValueError("Unknown DB engine: %s" % db_engine)

        settings.configure(
            DEBUG=True,
            DATABASES={'default': db_settings},
            CACHES={
                'default': {
                    'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
                }
            },
            MIDDLEWARE_CLASSES=['django.middleware.common.CommonMiddleware'],
            INSTALLED_APPS=(
                # Default Django apps from settings template
                # https://github.com/django/django/blob/2.1/django/conf/project_template/project_name/settings.py-tpl
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles') + self.APPS)

        django.setup()
        sys.exit(pytest.main(["tests/"]))


setup(
    name='django-richenum',
    version='3.6.0',
    description='Django Enum library for python.',
    long_description=(
        open('README.rst').read() + '\n\n' +
        open('CHANGELOG.rst').read() + '\n\n' +
        open('AUTHORS.rst').read()),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
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
