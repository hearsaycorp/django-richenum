Changelog
=========

4.1.0 (2023-12-12)
------------------
    - Support for Django 4.2
    - Support for Python 3.11
    - Remove support for Django 2.2, 3.0, 3.1
    - Remove support for Python 3.7
    - Require MySQL 8 and Postgres 12 

3.7.0 (2019-09-05)
------------------
    - Support for Django 2.3

3.6.0 (2019-07-09)
------------------
    - Support for Django 2.2
    - Support for Python 3.7
    - Remove support for Django 2.0

3.5.0 (2018-09-10)
------------------
    - Fix [deprecation of context param for Field.from_db_value](https://code.djangoproject.com/ticket/28370)
    - Support for Django 2.1
    - Switch tests suite to use pytest
    - Remove pylint-django plugin, no longer needed

3.4.0 (2018-02-10)
------------------
    - Drop support for old Django versions


3.3.0 (2018-01-21)
------------------
    - removed Python 3.4
    - add support for Python 3.6
    - add support for Django 2.0
    - Properly mark raw strings (used as regex)

3.2.0 (2016-08-22)
------------------
    - Python 3.4 & 3.5 support

3.1.0 (2015-08-02)
------------------
    - Django 1.10 support

3.0.1 (2015-07-13)
------------------
    - Prepare for python 3 support

2.4.1 (2015-05-04)
------------------
    - replace mysql client library (for tests)
    - stop using lambdas

2.3.0 (2015-05-04)
------------------
    - Support Django 1.8

2.2.0 (2015-03-11)
------------------
    - Support ModelForms for non-SQLite DB backends

2.1.0 (2014-11-01)
------------------
    - Support migration in Django 1.7

2.0.0 (2014-09-04)
------------------
    - Support Django 1.7, drop support for Python 2.6.

1.2.2 (2014-08-02)
------------------
    - Support Django 1.3

1.2.1 (2014-06-02)
------------------
    - Remove uses of BaseException.message.

1.2.0 (2013-12-03)
------------------
    - Add enum-aware versions of TypedMultipleChoiceField.

1.1.0 (2013-12-03)
------------------
    - Fix form fields to support Django 1.6 (while maintaining
      compatibility with 1.4 and 1.5).

1.0.2 (2013-11-05)
------------------
    - Make EnumField.run_validators a no-op.
      This stops some warnings from type comparison, and it doesn't seem
      useful in an EnumField context.

1.0.1 (2013-09-10)
------------------
    - Support South.

1.0.0 (2013-08-16)
------------------
    - Initial public release.
