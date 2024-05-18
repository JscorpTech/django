"""
Exceptions test
"""

import pytest
import unittest
from core import exceptions


class ExceptionTest(unittest.TestCase):
    def test_break_exception(self):
        with pytest.raises(exceptions.BreakException) as e:
            raise exceptions.BreakException("test message", data=[1, 2, 3])
        self.assertEqual(e.value.args[0], "test message")
