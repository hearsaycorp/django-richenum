from django import forms
from unittest import TestCase

from .models import NumNode


class NumNodeModelForm(forms.ModelForm):

    class Meta:
        model = NumNode
        # explicitly list the all fields for compatibility across Django version
        fields = ("num", "num_nullable", "num_lax", "num_str", "num_str_nullable", )


class ModelFormTests(TestCase):

    def test_model_form(self):
        form_data = {
            "num": "1",
            "num_nullable": "1",
            "num_lax": "1",
            "num_str": "one",
            "num_str_nullable": "one",
        }
        form = NumNodeModelForm(form_data)
        self.assertTrue(form.is_valid(), form.errors)
