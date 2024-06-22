"""
Utility test
"""

import unittest

from core.utils.cache import Cache


class UtilsTest(unittest.TestCase):
    def test_cache_remember(self):
        def mock_func():
            return "test"

        result = Cache.remember(mock_func, "test")
        self.assertEqual(result, "test")
