from requests.auth import AuthBase

try:
    # Python 2
    import urlparse

except ImportError:
    # Python 3
    import urllib.parse as urlparse


class DomainCredentials(AuthBase):
    allow_cookies = False
    credentials = None

    def __init__(self, credentials=None):
        self.credentials = credentials

    def __call__(self, request):
        if not self.credentials:
            return request

        # Include any authorization credentials relevant to this domain.
        url_components = urlparse.urlparse(request.url)
        host = url_components.hostname
        if host in self.credentials:
            request.headers['Authorization'] = self.credentials[host]
        return request
