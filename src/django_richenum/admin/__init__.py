from django.contrib import admin

from .filters import RichEnumFieldListFilter
from ..models.fields import IndexEnumField, LaxIndexEnumField, CanonicalNameEnumField
from .options import RichEnumModelAdmin

__all__ = [
    "RichEnumModelAdmin"
]


__registered = False


def register_admin_filters():
    """
    Registers RichEnum model field filters for usage with the Django admin UI
    The filters are registered only on the first call to this function
    """
    global __registered  # Use the module level __registered variable

    if not __registered:
        admin.FieldListFilter.register(
            lambda f: isinstance(f, (IndexEnumField, LaxIndexEnumField, CanonicalNameEnumField)),
            RichEnumFieldListFilter,
            take_priority=True)

        __registered = True
