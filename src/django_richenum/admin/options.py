from django.contrib import admin

import six

from ..models.fields import IndexEnumField, LaxIndexEnumField, CanonicalNameEnumField

RICH_ENUM_FORMFIELD_FOR_DBFIELD_DEFAULTS = {
    IndexEnumField: {},
    LaxIndexEnumField: {},
    CanonicalNameEnumField: {},
}


class RichEnumModelAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super(RichEnumModelAdmin, self).__init__(*args, **kwargs)

        # Update unspecified internal formfields
        for model_field_cls, formfield_override_value in six.iteritems(RICH_ENUM_FORMFIELD_FOR_DBFIELD_DEFAULTS):
            self.formfield_overrides.setdefault(model_field_cls, formfield_override_value)
