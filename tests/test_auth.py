#!/usr/bin/env python

import os
import tempfile
import unittest
from unittest import mock

import responses

from tank_utility import auth
from tank_utility import common


class AuthTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        auth.TOKEN_FILE_PATH = os.path.join(tempfile.gettempdir(), "tank_utility_token_test.txt")

    @staticmethod
    @responses.activate
    def test_get_token():
        responses.add(responses.GET, common.get_api_url(path="getToken"), status=200, json={"token": "token"})
        with mock.patch("tank_utility.auth._get_cached_token", autospec=True) as cached_token_mock, \
             mock.patch("tank_utility.auth._cache_token", autospec=True) as cache_token_mock:
            cached_token_mock.return_value = None
            auth.get_token("user", "password")
            cached_token_mock.assert_called_once_with("user")
            cache_token_mock.assert_called_once_with("token", "user")

    def test_token_cache_isolation(self):
        user_a = "UserA@Example.com "
        user_b = "userb@example.com"
        path_a = auth._get_token_file_path(user_a)
        path_b = auth._get_token_file_path(user_b)
        self.assertNotEqual(path_a, path_b)
        self.assertEqual(path_a, auth._get_token_file_path("usera@example.com"))
        self.assertEqual(auth._get_token_file_path(""), auth.TOKEN_FILE_PATH)

        try:
            auth._cache_token("token-a", user_a)
            auth._cache_token("token-b", user_b)
            self.assertEqual(auth._get_cached_token("usera@example.com"), "token-a")
            self.assertEqual(auth._get_cached_token(user_b), "token-b")
        finally:
            for p in (path_a, path_b):
                if os.path.exists(p):
                    os.remove(p)

    @staticmethod
    def test_get_token_timeout():
        with mock.patch("tank_utility.auth.requests.get", autospec=True) as get_mock, \
             mock.patch("tank_utility.auth._get_cached_token", return_value=None, autospec=True), \
             mock.patch("tank_utility.auth._cache_token", autospec=True):
            get_mock.return_value.json.return_value = {"token": "token"}
            auth.get_token("user", "password")
            assert get_mock.call_args[1]["timeout"] == common.DEFAULT_TIMEOUT

            auth.get_token("user", "password", timeout=5)
            assert get_mock.call_args[1]["timeout"] == 5


if __name__ == "__main__":
    unittest.main(verbosity=2)
