"""API authentication."""

import contextlib
import logging
import os
import os.path
import tempfile

import requests

from . import common

TOKEN_FILE_PATH = os.path.join(tempfile.gettempdir(), "tank_utility_token.txt")
"""Name of the file to store a cached token within."""


@contextlib.contextmanager
def umask(context_umask):
    """Modify umask within a context."""
    original_umask = os.umask(context_umask)
    try:
        yield
    finally:
        os.umask(original_umask)


def _get_cached_token():
    """Get a cached API token from a temporary file.

    :rtype: :py:class:`str`
    :returns: API token or empty string

    """
    token = ""
    try:
        with open(TOKEN_FILE_PATH, "r") as f:
            token = f.read()
    except FileNotFoundError:
        logging.info("No existing file %s", TOKEN_FILE_PATH)
    return token


def _cache_token(token):
    """Cache ``token`` in a temporary file.

    :param str token:

    """
    try:
        os.remove(TOKEN_FILE_PATH)
    except FileNotFoundError:
        logging.info("No existing file %s", TOKEN_FILE_PATH)
    with umask(0o077):
        with open(TOKEN_FILE_PATH, "w") as f:
            f.write(token)
        logging.info("Cached token in %s", TOKEN_FILE_PATH)


def get_token(username, password, force=False):
    """Get an API token.

    Unfortunately, the Tank Utility API only offers basic authentication and expires each API token after 24 hours.

    :param str username:
    :param str password:
    :param bool force: (optional) Get a new token even if one is currently cached
    :rtype: :py:class:`str`
    :returns: An API token
    :raises requests.exceptions.HTTPError:

    """
    token = None if force else _get_cached_token()
    if not token:
        response = requests.get(common.get_api_url(path="getToken"), auth=requests.auth.HTTPBasicAuth(username, password))
        response.raise_for_status()
        token = response.json()["token"]
        _cache_token(token)
    return token
