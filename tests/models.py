from django.db import models

from django_richenum.models import EnumField

from .constants import Number


class NumNode(models.Model):
    number = EnumField(Number, default=Number.ONE)
    parent = models.ForeignKey('self', null=True)


class NullableNumNode(models.Model):
    number = EnumField(Number, default=Number.ONE, null=True)
    parent = models.ForeignKey('self', null=True)
