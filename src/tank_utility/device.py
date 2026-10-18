"""Interact with Tank Utility devices."""

import requests

from . import auth
from . import common


def get_devices(token, timeout=common.DEFAULT_TIMEOUT):
    """Get devices associated with ``token``.

    :param str token:
    :param timeout: (optional) Connect/read timeout for API requests
    :rtype: :py:class:`list`
    :raises requests.exceptions.HTTPError:

    """
    response = requests.get(common.get_api_url(token=token, path="devices"), timeout=timeout)
    response.raise_for_status()
    return response.json()["devices"]


def get_device_data(token, device, timeout=common.DEFAULT_TIMEOUT):
    """Get ``device`` data.

    :param str token:
    :param str device:
    :param timeout: (optional) Connect/read timeout for API requests
    :rtype: :py:class:`dict`
    :raises requests.exceptions.HTTPError:

    """
    response = requests.get(common.get_api_url(token=token, path="devices/" + device), timeout=timeout)
    response.raise_for_status()
    return response.json()


def get_data(username, password, timeout=common.DEFAULT_TIMEOUT):
    """Get data for all devices associated with credentials.

    Get a new token if a cached token has expired.

    :param str username:
    :param str password:
    :param timeout: (optional) Connect/read timeout for API requests
    :rtype: :py:class:`dict`
    :returns: A mapping of device id to device data
    :raises requests.exceptions.HTTPError:

    """
    data = {}
    token = auth.get_token(username, password, timeout=timeout)
    try:
        devices = get_devices(token, timeout=timeout)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == requests.codes.unauthorized:  # pylint: disable=no-member
            token = auth.get_token(username, password, force=True, timeout=timeout)
            devices = get_devices(token, timeout=timeout)
        else:
            raise e
    for d in devices:
        try:
            data[d] = get_device_data(token, d, timeout=timeout)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == requests.codes.unauthorized:  # pylint: disable=no-member
                token = auth.get_token(username, password, force=True, timeout=timeout)
                data[d] = get_device_data(token, d, timeout=timeout)
            else:
                raise e
    return data
