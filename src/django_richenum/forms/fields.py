from abc import ABCMeta
from abc import abstractmethod

from django import forms
from django.core.exceptions import ValidationError
from richenum import EnumLookupError
from richenum import OrderedRichEnumValue

try:
    from django.forms.fields import RenameFieldMethods  # pylint: disable=no-name-in-module
except ImportError:
    # Fallback for Django versions < 1.8
    RenameFieldMethods = object


class CooperativeMeta(ABCMeta, RenameFieldMethods):
    pass


class _BaseEnumField(object):
    __metaclass__ = CooperativeMeta

    def _empty_value_factory(self):
        return None

    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        # Django default is empty string
        kwargs.setdefault('empty_value', self._empty_value_factory())  # pylint: disable=E1120

        if 'choices' in kwargs:
            raise ValueError('Cannot explicitly supply choices to enum fields.')
        if 'coerce' in kwargs:
            raise ValueError('Cannot explicitly supply coercion function to enum fields.')

        kwargs['choices'] = self.get_choices()
        kwargs['coerce'] = self.coerce_value
        super(_BaseEnumField, self).__init__(*args, **kwargs)

    @abstractmethod
    def get_choices(self):
        pass

    @abstractmethod
    def coerce_value(self, val):
        pass

    def run_validators(self, value):
        # These have to be from a set, so it's hard for me to imagine a useful
        # custom validator.
        # The run_validators method in the superclass checks the value against
        # None, [], {}, etc, which causes warnings in the RichEnum.__eq__
        # method... arguably we shouldn't warn in those cases, but for now we
        # do.
        pass

    def valid_value(self, value):
        return value in self.enum


class _BaseCanonicalField(_BaseEnumField):
    """
    Uses the RichEnum/OrderedRichEnum canonical_name as form field values
    """

    def get_choices(self):
        return self.enum.choices()

    def coerce_value(self, name):
        try:
            return self.enum.from_canonical(name)
        except EnumLookupError as e:
            raise ValidationError(str(e))

    # In Django 1.6, value is coerced already. Below 1.6, we need to manually coerce
    def valid_value(self, value):
        if isinstance(value, str):
            value = self.coerce_value(value)
        return super(_BaseCanonicalField, self).valid_value(value)


class _BaseIndexField(_BaseEnumField):
    """
    Uses the OrderedRichEnum index as form field values
    """

    def get_choices(self):
        return self.enum.choices(value_field='index')

    def coerce_value(self, index):
        try:
            return self.enum.from_index(int(index))
        except EnumLookupError as e:
            raise ValidationError(str(e))

    # In Django 1.6, value is coerced already. Below 1.6, we need to manually coerce
    def valid_value(self, value):
        # In < Dango 1.6, this comes in as a string, so we should flip it to be an int
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError as e:
                raise ValidationError(str(e))

        if isinstance(value, int):
            value = self.coerce_value(value)

        return super(_BaseIndexField, self).valid_value(value)

    def prepare_value(self, value):
        if isinstance(value, OrderedRichEnumValue):
            return value.index
        return super(_BaseIndexField, self).prepare_value(value)


class CanonicalEnumField(_BaseCanonicalField, forms.TypedChoiceField):
    pass


class IndexEnumField(_BaseIndexField, forms.TypedChoiceField):
    pass


class MultipleCanonicalEnumField(_BaseCanonicalField, forms.TypedMultipleChoiceField):
    def _empty_value_factory(self):
        return []


class MultipleIndexEnumField(_BaseIndexField, forms.TypedMultipleChoiceField):
    def _empty_value_factory(self):
        return []
