#!/usr/bin/env python

import unittest

from tank_utility import common


class CommonTestCase(unittest.TestCase):

    def test_get_api_url(self):
        expected = "https://data.tankutility.com/api"
        actual = common.get_api_url()
        self.assertEqual(expected, actual)

        expected = "https://data.tankutility.com/api?token=token"
        actual = common.get_api_url(token="token")
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main(verbosity=2)
