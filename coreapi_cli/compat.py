import json

try:
    # Python 3
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:
    # Python 2
    JSONDecodeError = ValueError


try:
    # Python 2
    import urlparse    # noqa
except ImportError:
    # Python 3
    import urllib.parse as urlparse  # noqa
