Changelog
=========

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
