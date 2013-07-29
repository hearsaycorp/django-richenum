from django import forms
from richenum.enums import _BaseRichEnumMetaclass


class EnumField(forms.TypedChoiceField):
    def __init__(self, enum_cls, *args, **kwargs):
        self.is_plain_enum = enum_cls.__name__ == 'Enum'
        self.is_rich_enum = isinstance(enum_cls, _BaseRichEnumMetaclass)

        kwargs.setdefault('empty_value', None)
        if 'choices' in kwargs:
            raise ValueError('Cannot explicitly supply choices to EnumField')
        if 'coerce' in kwargs:
            raise ValueError('Cannot explicitly supply coercion function to EnumField')

        if self.is_plain_enum:
            # coerce defaults to identity function, which is what we want for
            # plain enums
            kwargs['choices'] = [(v, k) for k, v in enum_cls.iteritems()]
            super(EnumField, self).__init__(*args, **kwargs)
        elif self.is_rich_enum:
            kwargs['coerce'] = enum_cls.from_canonical
            kwargs['choices'] = [(k.canonical_name, k.display_name) for k in enum_cls._MEMBERS]
            super(EnumField, self).__init__(*args, **kwargs)
        else:
            raise ValueError('Invalid enum class. Please use an enum, OrderedRichEnum, or RichEnum.')
