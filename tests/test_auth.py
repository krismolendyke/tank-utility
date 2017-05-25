#!/usr/bin/env python

import os
import tempfile
import unittest

import mock
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
            cached_token_mock.assert_called_once_with()
            cache_token_mock.assert_called_once_with("token")

if __name__ == "__main__":
    unittest.main(verbosity=2)
