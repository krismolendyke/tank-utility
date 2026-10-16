"""API authentication."""

import contextlib
import hashlib
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


def _get_token_file_path(username=""):
    """Get the path to the cached token file for ``username``.

    :param str username:
    :rtype: :py:class:`str`
    :returns: Path to cached token file

    """
    if not username:
        return TOKEN_FILE_PATH
    user_hash = hashlib.sha256(username.strip().lower().encode("utf-8")).hexdigest()[:12]
    return os.path.join(tempfile.gettempdir(), f"tank_utility_token_{user_hash}.txt")


def _get_cached_token(username=""):
    """Get a cached API token from a temporary file.

    :param str username:
    :rtype: :py:class:`str`
    :returns: API token or empty string

    """
    token = ""
    token_file_path = _get_token_file_path(username)
    try:
        with open(token_file_path, "r") as f:
            token = f.read()
    except FileNotFoundError:
        logging.info("No existing file %s", token_file_path)
    return token


def _cache_token(token, username=""):
    """Cache ``token`` in a temporary file.

    :param str token:
    :param str username:

    """
    token_file_path = _get_token_file_path(username)
    try:
        os.remove(token_file_path)
    except FileNotFoundError:
        logging.info("No existing file %s", token_file_path)
    with umask(0o077):
        with open(token_file_path, "w") as f:
            f.write(token)
        logging.info("Cached token in %s", token_file_path)


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
    token = None if force else _get_cached_token(username)
    if not token:
        response = requests.get(
            common.get_api_url(path="getToken"), auth=requests.auth.HTTPBasicAuth(username, password)
        )
        response.raise_for_status()
        token = response.json()["token"]
        _cache_token(token, username)
    return token
