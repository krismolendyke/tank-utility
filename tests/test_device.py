#!/usr/bin/env python

import os
import tempfile
import unittest
import unittest.mock

import requests
import responses

from tank_utility import auth
from tank_utility import common
from tank_utility import device


class DeviceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        auth.TOKEN_FILE_PATH = os.path.join(tempfile.gettempdir(), "tank_utility_token_test.txt")

    @responses.activate
    def test_get_devices(self):
        responses.add(responses.GET, common.get_api_url(path="devices"), status=200,
                      json={"devices": ["test0", "test1"]})
        expected = ["test0", "test1"]
        actual = device.get_devices("token")
        self.assertEqual(expected, actual)

    @responses.activate
    def test_get_data(self):
        responses.add(responses.GET, common.get_api_url(path="getToken"), status=requests.codes.ok,
                      json={"token": "token"})
        responses.add(responses.GET, common.get_api_url(path="devices"), status=requests.codes.ok,
                      json={"devices": ["test0", "test1"]})
        responses.add(responses.GET, common.get_api_url(path="devices/test0"), status=requests.codes.ok,
                      json={"k0": "v0"})
        responses.add(responses.GET, common.get_api_url(path="devices/test1"), status=requests.codes.ok,
                      json={"k1": "v1"})
        expected = {"test0": {"k0": "v0"}, "test1": {"k1": "v1"}}
        actual = device.get_data("token", "device")
        self.assertEqual(expected, actual)

    def test_get_data_retry(self):
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps, \
             unittest.mock.patch("tank_utility.device.auth._get_cached_token", autospec=True) as cached_token_mock:
            rsps.add(responses.GET, common.get_api_url(path="getToken"), status=requests.codes.ok,
                     json={"token": "expired-token"})
            rsps.add(responses.GET, common.get_api_url(path="devices"), status=requests.codes.unauthorized,
                     json={"devices": ["test0", "test1"]})
            rsps.add(responses.GET, common.get_api_url(path="getToken"), status=requests.codes.ok,
                     json={"token": "token"})
            rsps.add(responses.GET, common.get_api_url(path="devices"), status=requests.codes.ok,
                     json={"devices": ["test0", "test1"]})
            rsps.add(responses.GET, common.get_api_url(path="devices/test0"), status=requests.codes.ok,
                     json={"k0": "v0"})
            rsps.add(responses.GET, common.get_api_url(path="devices/test1"), status=requests.codes.ok,
                     json={"k1": "v1"})
            cached_token_mock.return_value = None
            expected = {"test0": {"k0": "v0"}, "test1": {"k1": "v1"}}
            actual = device.get_data("username", "password")
            self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main(verbosity=2)
