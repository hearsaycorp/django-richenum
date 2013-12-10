Changelog
=========

1.2.1 (2013-12-09)
------------------
    - Single element lists with an empty string in TypedMultipleChoiceField are considered empty values.

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
