# pylint: disable=R0903
"""
Utility functions for the CLI.
"""
import codecs
import json
import re
from termcolor import colored

import pyfiglet

def print_banner():
    """
    Prints a banner with the text "HAIONH1" using the "banner" font.
    """
    print("\n")
    banner = pyfiglet.figlet_format("H1ONH1", font="banner")
    print(colored(f"{banner}", 'light_magenta'))

def strip_surrounding_text(text):
    """
    Strips the surrounding text from a given string.

    Args:
        text (str): The input string.

    Returns:
        str: The resulting string with the surrounding text stripped.

    Raises:
        ValueError: If the input is not a string.
        TypeError: If the input is None.
        AttributeError: If the input does not have the required attributes.
    """
    try:
        pattern = r'{(.*?)}'
        match = re.search(pattern, text, re.DOTALL)
        if match is None:
            result = text
        else:
            result = "{" + match.group(1) + "}"
    except (ValueError, TypeError, AttributeError) as error:
        print(colored(f"Error! {error}", 'red'))
    return result


def parse_json_with_control_chars(json_string):
    """
    Parses a JSON string with control characters.

    Args:
        json_string (str): The JSON string to parse.

    Returns:
        dict or None: The parsed JSON data, or None if the JSON string is invalid.
    """

    try:
        json_string = codecs.escape_decode(json_string)[0].decode('UTF-8')
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        print(colored(f"Invalid JSON: {e}"), 'red')
        data = None
    return data
