from abc import ABCMeta
from abc import abstractmethod
from django import forms


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


class CanonicalEnumField(_BaseEnumField):
    """
    Uses the RichEnum/OrderedRichEnum canonical_name as form field values
    """

    def get_choices(self):
        return self.enum.choices()

    def coerce_value(self, name):
        return self.enum.from_canonical(name)


class IndexEnumField(_BaseEnumField):
    """
    Uses the OrderedRichEnum index as form field values
    """

    def get_choices(self):
        return self.enum.choices(value_field='index')

    def coerce_value(self, index):
        return self.enum.from_index(int(index))
