import numbers

from django.db import models

from richenum import OrderedRichEnum, OrderedRichEnumValue


class EnumField(models.IntegerField):
    '''Store ints in DB, but expose OrderedRichEnumValues in Python.

    '''
    description = 'Efficient storage for OrderedRichEnums'
    __metaclass__ = models.SubfieldBase

    enum = None  # Overridden in constructor

    def __init__(self, ordered_rich_enum, *args, **kwargs):
        if not issubclass(ordered_rich_enum, OrderedRichEnum):
            raise TypeError('%s is not an OrderedRichEnum')
        self.enum = ordered_rich_enum
        super(EnumField, self).__init__(*args, **kwargs)

    def get_default(self):
        '''Override Django's implementation, which casts all default values as
        unicode.

        '''
        if self.has_default():
            return self.default
        return None

    def get_prep_value(self, value):
        # Convert allowed types to integer for storage/queries
        if value is None:
            return None
        elif isinstance(value, numbers.Integral):
            return value
        elif isinstance(value, basestring):
            return self.enum.from_canonical(value).index
        elif isinstance(value, OrderedRichEnumValue):
            return value.index
        else:
            raise TypeError('Cannot convert value: %s (%s) to an Integer' % (value, type(value)))

    def to_python(self, value):
        # Convert from allowed types to OrderedRichEnumValue
        if value is None:
            return None
        elif isinstance(value, numbers.Integral):
            return self.enum.from_index(value)
        elif isinstance(value, basestring):
            return self.enum.from_canonical(value)
        elif isinstance(value, OrderedRichEnumValue):
            return value
        else:
            raise TypeError('Cannot interpret %s (%s) as an OrderedRichEnumValue' % (value, type(value)))
