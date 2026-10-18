#!/usr/bin/env python

import os
import tempfile
import unittest
from unittest import mock

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
        responses.add(
            responses.GET, common.get_api_url(path="devices"), status=200, json={"devices": ["test0", "test1"]}
        )
        expected = ["test0", "test1"]
        actual = device.get_devices("token")
        self.assertEqual(expected, actual)

    @responses.activate
    def test_get_data(self):
        responses.add(
            responses.GET, common.get_api_url(path="getToken"), status=requests.codes.ok, json={"token": "token"}
        )
        responses.add(
            responses.GET,
            common.get_api_url(path="devices"),
            status=requests.codes.ok,
            json={"devices": ["test0", "test1"]}
        )
        responses.add(
            responses.GET, common.get_api_url(path="devices/test0"), status=requests.codes.ok, json={"k0": "v0"}
        )
        responses.add(
            responses.GET, common.get_api_url(path="devices/test1"), status=requests.codes.ok, json={"k1": "v1"}
        )
        expected = {"test0": {"k0": "v0"}, "test1": {"k1": "v1"}}
        actual = device.get_data("token", "device")
        self.assertEqual(expected, actual)

    def test_get_data_retry(self):
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps, \
             mock.patch("tank_utility.device.auth._get_cached_token", autospec=True) as cached_token_mock:
            rsps.add(
                responses.GET,
                common.get_api_url(path="getToken"),
                status=requests.codes.ok,
                json={"token": "expired-token"}
            )
            rsps.add(
                responses.GET,
                common.get_api_url(token="expired-token", path="devices"),
                status=requests.codes.unauthorized,
                json={"devices": ["test0", "test1"]}
            )
            rsps.add(
                responses.GET, common.get_api_url(path="getToken"), status=requests.codes.ok, json={"token": "token"}
            )
            rsps.add(
                responses.GET,
                common.get_api_url(token="token", path="devices"),
                status=requests.codes.ok,
                json={"devices": ["test0", "test1"]}
            )
            rsps.add(
                responses.GET,
                common.get_api_url(token="token", path="devices/test0"),
                status=requests.codes.ok,
                json={"k0": "v0"}
            )
            rsps.add(
                responses.GET,
                common.get_api_url(token="token", path="devices/test1"),
                status=requests.codes.ok,
                json={"k1": "v1"}
            )
            cached_token_mock.return_value = None
            expected = {"test0": {"k0": "v0"}, "test1": {"k1": "v1"}}
            actual = device.get_data("username", "password")
            self.assertEqual(expected, actual)

    def test_get_data_device_detail_retry(self):
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps, \
             mock.patch("tank_utility.device.auth._get_cached_token", autospec=True) as cached_token_mock:
            rsps.add(
                responses.GET,
                common.get_api_url(path="getToken"),
                status=requests.codes.ok,
                json={"token": "expired-token"}
            )
            rsps.add(
                responses.GET,
                common.get_api_url(token="expired-token", path="devices"),
                status=requests.codes.ok,
                json={"devices": ["test0", "test1"]}
            )
            rsps.add(
                responses.GET,
                common.get_api_url(token="expired-token", path="devices/test0"),
                status=requests.codes.unauthorized
            )
            rsps.add(
                responses.GET,
                common.get_api_url(path="getToken"),
                status=requests.codes.ok,
                json={"token": "new-token"}
            )
            rsps.add(
                responses.GET,
                common.get_api_url(token="new-token", path="devices/test0"),
                status=requests.codes.ok,
                json={"k0": "v0"}
            )
            rsps.add(
                responses.GET,
                common.get_api_url(token="new-token", path="devices/test1"),
                status=requests.codes.ok,
                json={"k1": "v1"}
            )
            cached_token_mock.return_value = None
            expected = {"test0": {"k0": "v0"}, "test1": {"k1": "v1"}}
            actual = device.get_data("username", "password")
            self.assertEqual(expected, actual)

    @staticmethod
    def test_device_timeout():
        with mock.patch("tank_utility.device.requests.get", autospec=True) as get_mock:
            get_mock.return_value.json.return_value = {"devices": ["test0"]}
            device.get_devices("token")
            assert get_mock.call_args[1]["timeout"] == common.DEFAULT_TIMEOUT

            device.get_devices("token", timeout=15)
            assert get_mock.call_args[1]["timeout"] == 15

            get_mock.return_value.json.return_value = {"k0": "v0"}
            device.get_device_data("token", "test0")
            assert get_mock.call_args[1]["timeout"] == common.DEFAULT_TIMEOUT

            device.get_device_data("token", "test0", timeout=20)
            assert get_mock.call_args[1]["timeout"] == 20


if __name__ == "__main__":
    unittest.main(verbosity=2)
