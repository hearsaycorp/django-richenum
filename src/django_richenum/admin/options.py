from django.contrib import admin

from ..models.fields import CanonicalNameEnumField
from ..models.fields import IndexEnumField
from ..models.fields import LaxIndexEnumField

RICH_ENUM_FORMFIELD_FOR_DBFIELD_DEFAULTS = {
    IndexEnumField: {},
    LaxIndexEnumField: {},
    CanonicalNameEnumField: {},
}


class RichEnumModelAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super(RichEnumModelAdmin, self).__init__(*args, **kwargs)

        # Update unspecified internal formfields
        for model_field_cls, formfield_override_value in RICH_ENUM_FORMFIELD_FOR_DBFIELD_DEFAULTS.items():
            self.formfield_overrides.setdefault(model_field_cls, formfield_override_value)
