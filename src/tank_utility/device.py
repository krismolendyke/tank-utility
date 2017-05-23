"""Interact with Tank Utility devices."""

import requests

from . import auth
from . import common


def get_devices(token):
    """Get devices associated with ``token``.

    :param str token:
    :rtype: :py:class:`list`
    :raises requests.exceptions.HTTPError:

    """
    response = requests.get(common.get_api_url(token=token, path="devices"))
    response.raise_for_status()
    return response.json()["devices"]


def get_device_data(token, device):
    """Get ``device`` data.

    :param str token:
    :param str device:
    :rtype: :py:class:`dict`
    :raises requests.exceptions.HTTPError:

    """
    response = requests.get(common.get_api_url(token=token, path=f"devices/{device}"))
    response.raise_for_status()
    return response.json()


def get_data(username, password):
    """Get data for all devices associated with credentials.

    Get a new token if a cached token has expired.

    :param str username:
    :param str password:
    :rtype: :py:class:`dict`
    :returns: A mapping of device id to device data
    :raises requests.exceptions.HTTPError:

    """
    data = {}
    token = auth.get_token(username, password)
    try:
        devices = get_devices(token)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == requests.codes.unauthorized:
            devices = get_devices(auth.get_token(username, password, force=True))
        else:
            raise e
    for d in devices:
        data[d] = get_device_data(token, d)
    return data
