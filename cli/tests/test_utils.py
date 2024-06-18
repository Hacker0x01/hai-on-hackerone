"""
Utils test module
"""
import unittest
from unittest.mock import patch
from io import StringIO
import pyfiglet
from termcolor import colored

from utils import print_banner, strip_surrounding_text,parse_json_with_control_chars

class TestUtils(unittest.TestCase):
    """Test case for the utils module."""

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_banner(self, mock_stdout):
        """Test the print_banner function."""
        # Call the function
        print_banner()

        # Capture the printed output
        output = mock_stdout.getvalue()

        # Generate the expected banner using pyfiglet
        expected_banner = pyfiglet.figlet_format("H1ONH1", font="banner")
        expected_output = colored(f"{expected_banner}", 'light_magenta')

        # Verify the function output matches the expected output
        self.assertIn(expected_output.strip(), output.strip())

    def test_strip_surrounding_text(self):
        """Test the strip_surrounding_text function."""

        # Test case with surrounding text
        text = "This is {some text} surrounded by curly braces."
        expected_result = "{some text}"
        actual_result = strip_surrounding_text(text)
        self.assertEqual(actual_result, expected_result)

        # Test case without surrounding text
        text = "No surrounding text"
        expected_result = "No surrounding text"
        actual_result = strip_surrounding_text(text)
        self.assertEqual(actual_result, expected_result)

        # Test case with multiple sets of surrounding text
        text = "{First set} of {surrounding text} with {another set} of {curly braces}"
        expected_result = "{First set}"
        actual_result = strip_surrounding_text(text)
        self.assertEqual(actual_result, expected_result)

        # Test case with no text
        text = ""
        expected_result = ""
        actual_result = strip_surrounding_text(text)
        self.assertEqual(actual_result, expected_result)

        # Test case with None input
        text = None
        with self.assertRaises(TypeError):
            strip_surrounding_text(text)

        # Test case with invalid input type
        text = 123
        with self.assertRaises(ValueError):
            strip_surrounding_text(text)

        # Test case with input that does not have required attributes
        text = {"key": "value"}
        with self.assertRaises(ValueError):  # Change from AttributeError to ValueError
            strip_surrounding_text(text)

    def test_parse_json_with_control_chars(self):
        """Test the parse_json_with_control_chars function."""
        json_string = r'{"name": "John", "age": 30, "city": "New York"}'
        expected_data = {"name": "John", "age": 30, "city": "New York"}
        actual_data = parse_json_with_control_chars(json_string)
        self.assertEqual(actual_data, expected_data)

        invalid_json_string = r'{"name": "John", "age": 30, "city": "New York"'
        actual_data = parse_json_with_control_chars(invalid_json_string)
        self.assertIsNone(actual_data)
