from django import forms
from unittest import TestCase

from django_richenum.forms import CanonicalEnumField
from django_richenum.forms import IndexEnumField
from django_richenum.forms import MultipleCanonicalEnumField
from django_richenum.forms import MultipleIndexEnumField

from .constants import Number, Fruit


class CanonicalForm(forms.Form):
    num = CanonicalEnumField(Number)
    fruit = CanonicalEnumField(Fruit)
    fruit_optional = CanonicalEnumField(Fruit, required=False)
    fruit_default = CanonicalEnumField(Fruit, required=False, empty_value=Fruit.APPLE)


class CanonicalEnumFieldTests(TestCase):

    def test_coerces_with_canonical_name(self):
        form = CanonicalForm({'num': 'one', 'fruit': 'apple'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['num'], Number.ONE)
        self.assertEqual(form.cleaned_data['fruit'], Fruit.APPLE)

    def test_rich_enums_validate_by_canonical_name(self):
        # Can't pass in display name.
        form = CanonicalForm({'num': 'one', 'fruit': 'manzana'})
        self.assertFalse(form.is_valid())

    def test_ordered_enums_validate_by_canonical_name(self):
        # Can't pass in display name or index.
        display_form = CanonicalForm({'num': 'uno', 'fruit': 'apple'})
        index_form = CanonicalForm({'num': 2, 'fruit': 'apple'})

        self.assertFalse(display_form.is_valid())
        self.assertFalse(index_form.is_valid())

    def test_defaults_to_required(self):
        # By default, field is required.
        form = CanonicalForm({'num': 'one'})
        self.assertFalse(form.is_valid())

    def test_default_empty_value(self):
        # If not required, default empty value is None.
        form = CanonicalForm({'num': 'one', 'fruit': 'apple'})
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.cleaned_data['fruit_optional'])

    def test_can_override_default_empty_value(self):
        form = CanonicalForm({'num': 'one', 'fruit': 'apple'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['fruit_default'], Fruit.APPLE)

    def test_cant_pass_coerce_function(self):
        with self.assertRaises(ValueError):
            CanonicalEnumField(Fruit, coerce=int)

    def test_cant_pass_choices(self):
        choices = Fruit.choices()
        with self.assertRaises(ValueError):
            CanonicalEnumField(Fruit, choices=choices)


class IndexForm(forms.Form):
    num = IndexEnumField(Number)
    num_optional = IndexEnumField(Number, required=False)
    num_default = IndexEnumField(Number, required=False, empty_value=Number.ONE)


class IndexEnumFieldTests(TestCase):

    def test_coerces_with_index(self):
        form = IndexForm({'num': 1})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['num'], Number.ONE)

    def test_validates_with_index(self):
        # Can't pass in display or canonical names.
        canonical_form = IndexForm({'num': 'one'})
        display_form = IndexForm({'num': 'uno'})

        self.assertFalse(canonical_form.is_valid())
        self.assertFalse(display_form.is_valid())

    def test_defaults_to_required(self):
        # By default, field is required.
        form = IndexForm({})
        self.assertFalse(form.is_valid())

    def test_default_empty_value(self):
        # If not required, default empty value is None.
        form = IndexForm({'num': 1})
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.cleaned_data['num_optional'])

    def test_can_override_default_empty_value(self):
        form = IndexForm({'num': 1})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['num_default'], Number.ONE)

    def test_cant_pass_coerce_function(self):
        with self.assertRaises(ValueError):
            IndexEnumField(Number, coerce=int)

    def test_cant_pass_choices(self):
        choices = Number.choices()
        with self.assertRaises(ValueError):
            IndexEnumField(Number, choices=choices)


class MultipleCanonicalForm(forms.Form):
    num = MultipleCanonicalEnumField(Number)
    fruit = MultipleCanonicalEnumField(Fruit)
    fruit_optional = MultipleCanonicalEnumField(Fruit, required=False)
    fruit_default = MultipleCanonicalEnumField(Fruit, required=False, empty_value=(Fruit.APPLE,))


class MultiCanonicalFormTests(TestCase):

    def test_cant_pass_single_vals(self):
        form = MultipleCanonicalForm({'num': 'one', 'fruit': 'apple'})
        self.assertFalse(form.is_valid())

    def test_coerces_with_canonical_name(self):
        form = MultipleCanonicalForm({'num': ['one', 'two'], 'fruit': ['apple', 'peach']})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['num'], [Number.ONE, Number.TWO])
        self.assertEqual(form.cleaned_data['fruit'], [Fruit.APPLE, Fruit.PEACH])

    def test_rich_enums_validate_by_canonical_name(self):
        # Can't pass in display name.
        form = CanonicalForm({'num': ['one', 'two'], 'fruit': ['manzana', 'melocoton']})
        self.assertFalse(form.is_valid())

    def test_ordered_enums_validate_by_canonical_name(self):
        # Can't pass in display name or index.
        display_form = CanonicalForm({'num': ['uno', 'dos'], 'fruit': ['apple', 'peach']})
        index_form = CanonicalForm({'num': [1, 2], 'fruit': ['apple', 'peach']})

        self.assertFalse(display_form.is_valid())
        self.assertFalse(index_form.is_valid())

    def test_defaults_to_required(self):
        # By default, fruit is required.
        form = CanonicalForm({'num': ['one', 'two']})
        self.assertFalse(form.is_valid())

    def test_default_empty_value(self):
        form = MultipleCanonicalForm({'num': ['one', 'two'], 'fruit': ['apple', 'peach']})
        # If not required, default empty value is empty list.
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['fruit_optional'], [])

    def test_can_override_default_empty_value(self):
        form = MultipleCanonicalForm({'num': ['one', 'two'], 'fruit': ['apple', 'peach']})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['fruit_default'], (Fruit.APPLE,))

    def test_cant_pass_coerce_function(self):
        with self.assertRaises(ValueError):
            MultipleCanonicalEnumField(Fruit, coerce=int)

    def test_cant_pass_choices(self):
        choices = Fruit.choices()
        with self.assertRaises(ValueError):
            MultipleCanonicalEnumField(Fruit, choices=choices)


class MultipleIndexForm(forms.Form):
    num = MultipleIndexEnumField(Number)
    num_optional = MultipleIndexEnumField(Number, required=False)
    num_default = MultipleIndexEnumField(Number, required=False, empty_value=(Number.ONE, Number.TWO))


class MultiIndexFormTests(TestCase):

    def test_cant_pass_single_vals(self):
        form = MultipleIndexForm({'num': 1})
        self.assertFalse(form.is_valid())

    def test_coerces_with_index(self):
        form = MultipleIndexForm({'num': [1, 2]})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['num'], [Number.ONE, Number.TWO])

    def test_ordered_enums_validate_by_index(self):
        # Can't pass in display name or canonical name.
        display_form = CanonicalForm({'num': ['uno', 'dos']})
        canonical_form = CanonicalForm({'num': ['one', 'two']})

        self.assertFalse(display_form.is_valid())
        self.assertFalse(canonical_form.is_valid())

    def test_defaults_to_required(self):
        # By default, num is required.
        form = CanonicalForm({})
        self.assertFalse(form.is_valid())

    def test_default_empty_value(self):
        form = MultipleIndexForm({'num': [1, 2]})
        # If not required, default empty value is empty list.
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['num_optional'], [])

    def test_can_override_default_empty_value(self):
        form = MultipleIndexForm({'num': [1, 2]})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['num_default'], (Number.ONE, Number.TWO))

    def test_cant_pass_coerce_function(self):
        with self.assertRaises(ValueError):
            MultipleIndexEnumField(Number, coerce=int)

    def test_cant_pass_choices(self):
        choices = Number.choices()
        with self.assertRaises(ValueError):
            MultipleIndexEnumField(Number, choices=choices)
