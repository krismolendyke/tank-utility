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

    def test_version(self):
        import tank_utility

        self.assertEqual(tank_utility.__version__, "1.5.3")
        self.assertEqual(common.DEFAULT_TIMEOUT, (10, 30))


if __name__ == "__main__":
    unittest.main(verbosity=2)
