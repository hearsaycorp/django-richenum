from abc import ABCMeta
from abc import abstractmethod
from django import forms
from django.core.exceptions import ValidationError

from richenum import EnumLookupError


class _BaseEnumField(forms.TypedChoiceField):
    __metaclass__ = ABCMeta

    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        kwargs.setdefault('empty_value', None)

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


class CanonicalEnumField(_BaseEnumField):
    """
    Uses the RichEnum/OrderedRichEnum canonical_name as form field values
    """

    def get_choices(self):
        return self.enum.choices()

    def coerce_value(self, name):
        try:
            return self.enum.from_canonical(name)
        except EnumLookupError as e:
            raise ValidationError(e.message)

    # In Django 1.6, value is coerced already. Below 1.6, we need to manually coerce
    def valid_value(self, value):
        if isinstance(value, basestring):
            value = self.coerce_value(value)
        return super(CanonicalEnumField, self).valid_value(value)


class IndexEnumField(_BaseEnumField):
    """
    Uses the OrderedRichEnum index as form field values
    """

    def get_choices(self):
        return self.enum.choices(value_field='index')

    def coerce_value(self, index):
        try:
            return self.enum.from_index(int(index))
        except EnumLookupError as e:
            raise ValidationError(e.message)

    # In Django 1.6, value is coerced already. Below 1.6, we need to manually coerce
    def valid_value(self, value):
        # In < Dango 1.6, this comes in as a string, so we should flip it to be an int
        if isinstance(value, basestring):
            try:
                value = int(value)
            except ValueError as e:
                raise ValidationError(e.message)

        if isinstance(value, int):
            value = self.coerce_value(value)

        return super(IndexEnumField, self).valid_value(value)
