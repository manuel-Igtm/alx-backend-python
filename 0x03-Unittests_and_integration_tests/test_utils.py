#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
      ({"a": 1}, ("a",), 1),
      ({"a": {"b": 2}}, ("a",), {"b": 2}),
      ({"a": {"b": 2}}, ("a", "b"), 2),
   
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("missing_key_1", {}, ("a",), "a"),
        ("missing_key_2", {"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, name, nested_map, path, expected_msg):
        """Test access_nested_map raises KeyError as expected"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(expected_msg))


class TestGetJson(unittest.TestCase):
    """Test get_json function for HTTP request mocking"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test get_json returns expected result with mocked requests.get"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch("utils.requests.get", return_value=mock_response) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test the memoization functionality"""

    def test_memoize(self):
        """Test that memoization caches result and calls original method only once"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            result_1 = obj.a_property
            result_2 = obj.a_property
            self.assertEqual(result_1, 42)
            self.assertEqual(result_2, 42)
            mock_method.assert_called_once()
