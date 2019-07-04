__version__ = 'unknown'
try:
    __version__ = __import__('pkg_resources').get_distribution('django_richenum').version
except Exception:
    pass
