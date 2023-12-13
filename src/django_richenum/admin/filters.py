from django import forms
from django.contrib import admin
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _

from ..forms.fields import IndexEnumField as IndexEnumFormField
from ..forms.fields import CanonicalEnumField as CanonicalNameEnumFormField

from richenum import RichEnum, OrderedRichEnum


class RichEnumFieldListFilter(admin.FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.enum = field.enum
        self.lookup_kwarg = field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg)

        # Create a Django form to validate request params
        form_cls_name = "%sRichEnumFieldListFilterForm" % self.enum.__name__
        form_attrs = {}
        if issubclass(self.enum, OrderedRichEnum):
            form_attrs[self.lookup_kwarg] = IndexEnumFormField(self.enum)
        elif issubclass(self.enum, RichEnum):
            form_attrs[self.lookup_kwarg] = CanonicalNameEnumFormField(self.enum)

        self.form_cls = type(form_cls_name, (forms.Form, ), form_attrs)

        super(RichEnumFieldListFilter, self).__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def choices(self, cl):
        yield {
            "selected": self.lookup_val is None,
            "query_string": cl.get_query_string({}, [self.lookup_kwarg]),
            "display": _("All"),
        }

        # Generate choices based off of RichEnum
        # Note: if the RichEnumValues are modified, the data stored in the DB may be out of sync from the RichEnum
        choices = ()
        if issubclass(self.enum, OrderedRichEnum):
            choices = self.enum.choices("index")
        elif issubclass(self.enum, RichEnum):
            choices = self.enum.choices()

        for lookup, title in choices:
            yield {
                "selected": smart_str(lookup) == self.lookup_val,
                "query_string": cl.get_query_string({
                    self.lookup_kwarg: lookup}),
                "display": title,
            }

    def queryset(self, request, queryset):
        kwargs = {}

        # Validate filter params
        form = self.form_cls(request.GET)
        if form.is_valid():
            kwargs[self.lookup_kwarg] = form.cleaned_data[self.lookup_kwarg]

        return queryset.filter(**kwargs)
