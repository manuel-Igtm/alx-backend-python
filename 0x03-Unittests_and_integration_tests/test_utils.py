#!/usr/bin/env python3
"""Unit tests for the access_nested_map function in the utils module."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .utils import access_nested_map

import unittest
from parameterized import parameterized
from .utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test case for the access_nested_map function."""

    @parameterized.expand([
        ("simple_path", {"a": 1}, ("a",), 1),
        ("nested_path_level1", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("nested_path_level2", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        """Test that access_nested_map returns the expected result for valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main()
