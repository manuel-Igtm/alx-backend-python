#!/usr/bin/env python3
"""
This module contains unit tests for the utility functions in utils.py.
It verifies correct behavior for nested map access, JSON fetching,
and memoization behavior.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ("nested_map with single key", {"a": 1}, ("a",), 1),
        ("nested_map with nested dict", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("nested_map full path", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, name: str, nested_map: dict, path: tuple, expected: object) -> None:
        """Test successful access to values in a nested map."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("empty nested_map", {}, ("a",), "a"),
        ("missing nested key", {"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, name: str, nested_map: dict, path: tuple, missing_key: str) -> None:
        """Test KeyError is raised for missing keys in the path."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(missing_key))


class TestGetJson(unittest.TestCase):
    """Tests for the get_json function that fetches JSON from a URL."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: dict) -> None:
        """Test that get_json returns the expected payload from a URL."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch("utils.requests.get", return_value=mock_response) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator."""

    def test_memoize(self) -> None:
        """Test that memoized method is only called once."""

        class TestClass:
            """Simple class to test memoization."""

            def a_method(self) -> int:
                """Method returning constant for test purposes."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Memoized method returning result of a_method."""
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            test_instance = TestClass()
            self.assertEqual(test_instance.a_property(), 42)
            self.assertEqual(test_instance.a_property(), 42)
            mock_method.assert_called_once()