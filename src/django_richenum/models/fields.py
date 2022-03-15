from django.db import models
from richenum import OrderedRichEnumValue
from richenum import RichEnumValue


# https://github.com/django/django/blob/64200c14e0072ba0ffef86da46b2ea82fd1e019a/django/db/models/fields/subclassing.py#L31-L44
class Creator(object):
    """
    A placeholder class that provides a way to set the attribute on the model.
    """
    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)


class IndexEnumField(models.IntegerField):
    '''Store ints in DB, but expose OrderedRichEnumValues in Python.

    '''
    description = 'Efficient storage for OrderedRichEnums'

    def contribute_to_class(self, cls, name, **kwargs):
        super(IndexEnumField, self).contribute_to_class(cls, name, **kwargs)

        # Add Creator descriptor to allow the field to be set directly
        setattr(cls, self.name, Creator(self))

    def __init__(self, enum, *args, **kwargs):
        if not hasattr(enum, 'from_index'):
            raise TypeError("%s doesn't support index-based lookup." % enum)
        self.enum = enum
        super(IndexEnumField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(IndexEnumField, self).deconstruct()
        args.insert(0, self.enum)

        return name, path, args, kwargs

    def get_default(self):
        # Override Django's implementation, which casts all default values to
        # unicode.
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.default
        return None

    def get_prep_value(self, value):
        # Convert value to integer for storage/queries.
        if value is None:
            return None
        elif isinstance(value, OrderedRichEnumValue):
            return value.index
        elif isinstance(value, int):
            return value
        else:
            raise TypeError('Cannot convert value: %s (%s) to an int.' % (value, type(value)))

    def from_db_value(self, value, expression, connection, *args):
        # context param is deprecated in Django 2.x will be removed in Django 3.x
        # having *args allows this code to run in Django 1.x and Django 2.x
        if value is None:
            return value
        return self.enum.from_index(value)

    def to_python(self, value):
        # Convert value to OrderedRichEnumValue. (Called on *all* assignments
        # to the field, including object creation from a DB record.)
        if value is None:
            return None
        elif isinstance(value, OrderedRichEnumValue):
            return value
        elif isinstance(value, int):
            return self.enum.from_index(value)
        else:
            raise TypeError('Cannot interpret %s (%s) as an OrderedRichEnumValue.' % (value, type(value)))

    def run_validators(self, value):
        """
        Validate that the value is of the correct type for Model field validation
        Model fields are only validated during ModelForm.clean().
        https://docs.djangoproject.com/en/1.7/ref/validators/#how-validators-are-run
        The value used for validation hasn't been converted for DB storage yet
        but is validated using validators that are DB specific.
        So we need to cast the value to one used for DB storage.
        """
        if isinstance(value, OrderedRichEnumValue):
            value = value.index
        return super(IndexEnumField, self).run_validators(value)

    def formfield(self, **kwargs):
        # import here to avoid circular imports
        from django_richenum.forms.fields import IndexEnumField as IndexEnumFormField

        defaults = {"enum": self.enum, "form_class": IndexEnumFormField,
                    "choices_form_class": IndexEnumFormField}
        return super(IndexEnumField, self).formfield(**defaults)


class LaxIndexEnumField(IndexEnumField):
    '''Like IndexEnumField, but also allows casting to and from
    canonical names.

    Mainly used to help migrate existing code that uses strings as database values.
    '''
    def get_prep_value(self, value):
        if isinstance(value, str):
            return self.enum.from_canonical(value).index
        return super(LaxIndexEnumField, self).get_prep_value(value)

    def from_db_value(self, value, expression, connection, *args):
        # context param is deprecated in Django 2.x will be removed in Django 3.x
        # having *args allows this code to run in Django 1.x and Django 2.x
        if isinstance(value, str):
            return self.enum.from_canonical(value)
        return super(LaxIndexEnumField, self).from_db_value(value, expression, connection, *args)

    def to_python(self, value):
        if isinstance(value, str):
            return self.enum.from_canonical(value)
        return super(LaxIndexEnumField, self).to_python(value)


class CanonicalNameEnumField(models.CharField):
    '''Store varchar in DB, but expose RichEnumValues in Python.

    '''
    description = 'Storage for RichEnums'

    def contribute_to_class(self, cls, name, **kwargs):
        super(CanonicalNameEnumField, self).contribute_to_class(cls, name, **kwargs)

        # Add Creator descriptor to allow the field to be set directly
        setattr(cls, self.name, Creator(self))

    def __init__(self, enum, *args, **kwargs):
        if not hasattr(enum, 'from_canonical'):
            raise TypeError("%s doesn't support canonical_name lookup." % enum)
        self.enum = enum
        super(CanonicalNameEnumField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(CanonicalNameEnumField, self).deconstruct()
        args.insert(0, self.enum)

        return name, path, args, kwargs

    def get_default(self):
        # Override Django's implementation, which casts all default values to
        # unicode.
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.default
        return None

    def get_prep_value(self, value):
        # Convert value to string for storage/queries.
        if value is None:
            return None
        elif isinstance(value, RichEnumValue):
            return value.canonical_name
        elif isinstance(value, str):
            return value
        else:
            raise TypeError('Cannot convert value: %s (%s) to a string.' % (value, type(value)))

    def from_db_value(self, value, expression, connection, *args):
        # context param is deprecated in Django 2.x will be removed in Django 3.x
        # having *args allows this code to run in Django 1.x and Django 2.x
        if value is None:
            return value
        return self.enum.from_canonical(value)

    def to_python(self, value):
        # Convert value to RichEnumValue. (Called on *all* assignments
        # to the field, including object creation from a DB record.)
        if value is None:
            return None
        elif isinstance(value, RichEnumValue):
            return value
        elif isinstance(value, str):
            return self.enum.from_canonical(value)
        else:
            raise TypeError('Cannot interpret %s (%s) as an RichEnumValue.' % (value, type(value)))

    def run_validators(self, value):
        """
        Validate that the value is of the correct type for Model field validation
        Model fields are only validated during ModelForm.clean().
        https://docs.djangoproject.com/en/1.7/ref/validators/#how-validators-are-run
        The value used for validation hasn't been converted for DB storage yet
        but is validated using validators that are DB specific.
        So we need to cast the value to one used for DB storage.
        """
        if isinstance(value, RichEnumValue):
            value = value.canonical_name
        return super(CanonicalNameEnumField, self).run_validators(value)

    def formfield(self, **kwargs):
        # import here to avoid circular imports
        from django_richenum.forms.fields import CanonicalEnumField as CanonicalEnumFormField

        defaults = {"enum": self.enum, "form_class": CanonicalEnumFormField,
                    "choices_form_class": CanonicalEnumFormField}
        # Don't use super(CanonicalNameEnumField, self) since
        # that'll send the unsupported max_length kwarg to the CanonicalEnumFormField
        return super(models.CharField, self).formfield(**defaults)  # pylint: disable=E1003


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [
        r"^django_richenum\.models\.fields\.IndexEnumField",
        r"^django_richenum\.models\.fields\.LaxIndexEnumField",
        r"^django_richenum\.models\.fields\.CanonicalNameEnumField",
    ])
except ImportError:
    pass
