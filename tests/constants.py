from richenum import OrderedRichEnum, OrderedRichEnumValue


class _Number(OrderedRichEnumValue):
    pass


class Number(OrderedRichEnum):
    ONE = _Number(1, 'one', 'uno')
    TWO = _Number(2, 'two', 'deux')
