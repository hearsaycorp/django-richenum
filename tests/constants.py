from richenum import OrderedRichEnum
from richenum import OrderedRichEnumValue
from richenum import RichEnum
from richenum import RichEnumValue


class _Number(OrderedRichEnumValue):
    pass


class Number(OrderedRichEnum):
    ONE = _Number(1, 'one', 'uno')
    TWO = _Number(2, 'two', 'deux')


class _Fruit(RichEnumValue):
    pass


class Fruit(RichEnum):
    APPLE = _Fruit('apple', 'manzana')
    PEACH = _Fruit('peach', 'melocoton')
