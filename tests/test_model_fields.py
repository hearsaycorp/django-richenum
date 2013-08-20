from django.db import IntegrityError
from django.test import TestCase

from richenum import OrderedRichEnumValue

from .constants import Number
from .models import NumNode, NullableNumNode


class OrderedEnumTests(TestCase):
    def test_inits_with_default(self):
        # Verify that we can supply a default value
        default_instance = NumNode()
        self.assertEqual(default_instance.number, Number.ONE)
        self.assertTrue(isinstance(default_instance.number, OrderedRichEnumValue))

    def test_fetch_with_enum(self):
        # Support fetching with enum, not index
        m = NumNode(number=Number.ONE)
        m.save()
        display_name = NumNode.objects.get(number=Number.ONE).number.display_name  # pylint: disable=E1101
        self.assertEqual(display_name, 'uno')

    def test_joins_with_enum(self):
        # Also support joins
        first = NumNode()
        first.save()
        second = NumNode(number=Number.TWO, parent=first)
        second.save()
        num_children = NumNode.objects.filter(parent__number=Number.ONE).count()  # pylint: disable=E1101
        self.assertEqual(num_children, 1)

    def test_allows_index(self):
        # Though it breaks abstraction, allow using index instead of enum
        m = NumNode(number=1)
        m.save()
        self.assertEqual(m.number.display_name, 'uno')
        self.assertEqual(NumNode.objects.filter(number=1).count(), 1)  # pylint: disable=E1101

    def test_allows_canonical(self):
        # Also allow using canonical name
        m = NumNode(number='one')
        m.save()
        self.assertEqual(m.number.display_name, 'uno')
        self.assertEqual(NumNode.objects.filter(number='one').count(), 1)  # pylint: disable=E1101

    def test_default_forbids_nulls(self):
        with self.assertRaises(IntegrityError):
            null = NumNode(number=None)
            null.save()

    def test_can_allow_nulls(self):
        null_instance = NullableNumNode(number=None)
        null_instance.save()
        self.assertIsNone(null_instance.number)
