from django.db import models

from django_richenum.models import IndexEnumField
from django_richenum.models import LaxIndexEnumField
from django_richenum.models import CanonicalNameEnumField

from .constants import Number


class NumNode(models.Model):
    num = IndexEnumField(Number, default=Number.ONE)
    num_nullable = IndexEnumField(Number, default=Number.ONE, null=True)
    num_lax = LaxIndexEnumField(Number, default=Number.ONE)
    num_str = CanonicalNameEnumField(Number, default=Number.ONE, max_length=5)
    num_str_nullable = CanonicalNameEnumField(Number, default=Number.ONE, max_length=5, null=True)
    parent = models.ForeignKey('self', null=True)
