===============
django-richenum
===============

.. image:: https://travis-ci.org/hearsaycorp/django-richenum.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/hearsaycorp/django-richenum

.. image:: https://pypip.in/v/django-richenum/badge.png
    :alt: Latest PyPI Version
    :target: https://pypi.python.org/pypi/django-richenum/

=====
About
=====
A Django extension of richenum for Python. If you're unfamiliar with richenums, please read up on them (see `Related Packages`_) before using django-richenum.

-----------
Model Fields
-----------
IndexEnumField
  Store ints in DB, but expose OrderedRichEnumValues in Python.
CanonicalNameEnumField
  Store varchar in DB, but expose RichEnumValues in Python.
  We recommend that you use IndexEnumField for storage and query efficiency.
LaxIndexEnumField
  Like IndexEnumField, but also allows casting to and from canonical names.
  Mainly used to help migrate existing code that uses strings as database values.

-----------
Form Fields
-----------
CanonicalEnumField
  Uses the RichEnum/OrderedRichEnum canonical_name as form field values.
IndexEnumField
  Uses the OrderedRichEnum index as form field values.

-----
Links
-----
| `GitHub <https://github.com/hearsaycorp/django-richenum>`_
| `PyPi <https://pypi.python.org/pypi/django-richenum/>`_

============
Installation
============
.. code:: bash

    $ pip install django-richenum

=============
Example Usage
=============
--------------
IndexEnumField
--------------
.. code:: python

    >>> from richenum import OrderedRichEnum, OrderedRichEnumValue
    >>> class MyOrderedRichEnum(OrderedRichEnum):
    ...    FOO = OrderedRichEnumValue(index=1, canonical_name="foo", display_name="Foo")
    ...    BAR = OrderedRichEnumValue(index=2, canonical_name="bar", display_name="Bar")
    ...
    >>> from django.db import models
    >>> from django_richenum.models import IndexEnumField
    >>> class MyModel(models.Model):
    ...    my_enum = IndexEnumField(MyOrderedRichEnum, default=MyOrderedRichEnum.FOO)
    ...
    >>> m = MyModel.objects.create(my_enum=MyOrderedRichEnum.BAR)
    >>> m.save()
    >>> m.my_enum
    OrderedRichEnumValue - idx: 2  canonical_name: 'bar'  display_name: 'Bar'
    >>> MyModel.objects.filter(my_enum=MyOrderedRichEnum.BAR)


----------------------
CanonicalNameEnumField
----------------------
.. code:: python

    >>> from richenum import RichEnum, RichEnumValue
    >>> class MyRichEnum(RichEnum):
    ...    FOO = RichEnumValue(canonical_name="foo", display_name="Foo")
    ...    BAR = RichEnumValue(canonical_name="bar", display_name="Bar")
    ...
    >>> from django.db import models
    >>> from django_richenum.models import CanonicalNameEnumField
    >>> class MyModel(models.Model):
    ...    my_enum = CanonicalNameEnumField(MyRichEnum, default=MyRichEnum.FOO)
    ...
    >>> m = MyModel.objects.create(my_enum=MyRichEnum.BAR)
    >>> m.save()
    >>> m.my_enum
    RichEnumValue - canonical_name: 'bar'  display_name: 'Bar'
    >>> MyModel.objects.filter(my_enum=MyRichEnum.BAR)


================
Related Packages
================

richenum
  Package implementing RichEnum and OrderedRichEnum that django-richenum depends on.

  | `GitHub <https://github.com/hearsaycorp/richenum>`_

  | `PyPi <https://pypi.python.org/pypi/richenum/>`_


============
Contributing
============

#. Fork the repo from `GitHub <https://github.com/hearsaycorp/django-richenum>`_.
#. Make your changes.
#. Add unittests for your changes.
#. Run `pep8 <https://pypi.python.org/pypi/pep8>`_, `pyflakes <https://pypi.python.org/pypi/pyflakes>`_, and `pylint <https://pypi.python.org/pypi/pyflakes>`_ to make sure your changes follow the Python style guide and doesn't have any errors.
#. Add yourself to the AUTHORS file (in alphabetical order).
#. Send a pull request from your fork to the main repo.
