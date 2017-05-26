"""Common functions."""

try:
    from urllib.parse import SplitResult, urlencode, urlunsplit
except ImportError:
    from urllib import urlencode
    from urlparse import SplitResult, urlunsplit

PROPANE_API_PROTOCOL = "https"
PROPANE_API_LOCATION = "data.tankutility.com"
"""The base location of the propane API."""


def get_api_url(token="", path=""):
    """Get an API URL for the given path.

    :param str token: (optional) API token
    :param str path: (optional) API path
    :rtype: :py:class:`str`
    :returns: An API URL

    """
    query = urlencode({"token": token}) if token else ""
    api_path = "/".join(["api", path]).strip("/")
    split = SplitResult(
        scheme=PROPANE_API_PROTOCOL, netloc=PROPANE_API_LOCATION, path=api_path, query=query, fragment=""
    )
    return urlunsplit(split)
