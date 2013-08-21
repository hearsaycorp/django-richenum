from django.db import models

from django_richenum.models import IndexEnumField
from django_richenum.models import LaxIndexEnumField

from .constants import Number


class NumNode(models.Model):
    num = IndexEnumField(Number, default=Number.ONE)
    num_nullable = IndexEnumField(Number, default=Number.ONE, null=True)
    num_lax = LaxIndexEnumField(Number, default=Number.ONE)
    parent = models.ForeignKey('self', null=True)
