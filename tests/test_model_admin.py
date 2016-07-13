from django.contrib import admin
from django.test import TestCase

from .models import NumNode
from django_richenum.admin import RichEnumModelAdmin


class ModelAdminTests(TestCase):
    def test_register(self):
        admin.site.register(NumNode, RichEnumModelAdmin)
