import forms  # noqa
import models  # noqa


__all__ = (
    'forms',
    'models',
)


__version__ = 'unknown'
try:
    __version__ = __import__('pkg_resources').get_distribution('django_richenum').version
except Exception as e:
    pass
