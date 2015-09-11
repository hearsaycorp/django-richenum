from django.db import IntegrityError
from django.test import TestCase

from .constants import Number
from .models import NumNode


class IndexFieldTests(TestCase):
    def test_inits_with_default(self):
        default_instance = NumNode()
        self.assertEqual(default_instance.num, Number.ONE)

    def test_inits_with_callable_default(self):
        default_instance = NumNode()
        self.assertEqual(default_instance.num_callable_default, Number.ONE)

    def test_assignment_allows_enum_values(self):
        default_instance = NumNode()
        default_instance.num = Number.TWO
        self.assertEqual(default_instance.num, Number.TWO)

    def test_assignment_casts_ints_to_enum_values(self):
        default_instance = NumNode()
        default_instance.num = 2
        self.assertEqual(default_instance.num, Number.TWO)

    def test_fetch_casts_ints_back_to_enum_values(self):
        m = NumNode(num=Number.ONE)
        m.save()
        display_name = NumNode.objects.get(num=Number.ONE).num.display_name
        self.assertEqual(display_name, 'uno')

    def test_queries_with_enum_values(self):
        m = NumNode(num=Number.ONE)
        m.save()
        self.assertEqual(NumNode.objects.filter(num=Number.ONE).count(), 1)

    def test_queries_with_ints(self):
        m = NumNode(num=Number.ONE)
        m.save()
        self.assertEqual(NumNode.objects.filter(num=1).count(), 1)

    def test_joins_with_enum_values(self):
        first = NumNode()
        first.save()
        second = NumNode(num=Number.TWO, parent=first)
        second.save()
        num_children = NumNode.objects.filter(parent__num=Number.ONE).count()
        self.assertEqual(num_children, 1)

    def test_joins_with_ints(self):
        first = NumNode()
        first.save()
        second = NumNode(num=Number.TWO, parent=first)
        second.save()
        num_children = NumNode.objects.filter(parent__num=1).count()
        self.assertEqual(num_children, 1)

    def test_default_forbids_nulls(self):
        with self.assertRaises(IntegrityError):
            null = NumNode(num=None)
            null.save()

    def test_can_allow_nulls(self):
        null_instance = NumNode(num=Number.ONE, num_nullable=None)
        null_instance.save()
        self.assertIsNone(null_instance.num_nullable)


def LaxIndexFieldTests(TestCase):
    def test_allows_canonical(self):
        # Also allow using canonical name.
        m = NumNode(num='one')
        m.save()
        self.assertEqual(m.num.display_name, 'uno')
        self.assertEqual(NumNode.objects.filter(num='one').count(), 1)


class CanonicalNameFieldTests(TestCase):
    def test_inits_with_default(self):
        default_instance = NumNode()
        self.assertEqual(default_instance.num_str, Number.ONE)

    def test_inits_with_callable_default(self):
        default_instance = NumNode()
        self.assertEqual(default_instance.num_str_callable_default, Number.ONE)

    def test_assignment_allows_enum_values(self):
        default_instance = NumNode()
        default_instance.num_str = Number.TWO
        self.assertEqual(default_instance.num_str, Number.TWO)

    def test_assignment_casts_strs_to_enum_values(self):
        default_instance = NumNode()
        default_instance.num_str = "two"
        self.assertEqual(default_instance.num_str, Number.TWO)

    def test_fetch_casts_strs_back_to_enum_values(self):
        m = NumNode(num_str=Number.ONE)
        m.save()
        display_name = NumNode.objects.get(num_str=Number.ONE).num_str.display_name
        self.assertEqual(display_name, 'uno')

    def test_queries_with_enum_values(self):
        m = NumNode(num_str=Number.ONE)
        m.save()
        self.assertEqual(NumNode.objects.filter(num_str=Number.ONE).count(), 1)

    def test_queries_with_strs(self):
        m = NumNode(num_str=Number.ONE)
        m.save()
        self.assertEqual(NumNode.objects.filter(num_str='one').count(), 1)

    def test_joins_with_enum_values(self):
        first = NumNode()
        first.save()
        second = NumNode(num_str=Number.TWO, parent=first)
        second.save()
        num_children = NumNode.objects.filter(parent__num_str=Number.ONE).count()
        self.assertEqual(num_children, 1)

    def test_joins_with_strs(self):
        first = NumNode()
        first.save()
        second = NumNode(num_str=Number.TWO, parent=first)
        second.save()
        num_children = NumNode.objects.filter(parent__num_str='one').count()
        self.assertEqual(num_children, 1)

    def test_default_forbids_nulls(self):
        with self.assertRaises(IntegrityError):
            null = NumNode(num_str=None)
            null.save()

    def test_can_allow_nulls(self):
        null_instance = NumNode(num_str=Number.ONE, num_str_nullable=None)
        null_instance.save()
        self.assertIsNone(null_instance.num_str_nullable)
