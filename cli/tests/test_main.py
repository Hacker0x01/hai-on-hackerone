# pylint: disable=W0718,W0613

"""
Main test module
"""
import unittest
import argparse
import io
import sys
from unittest.mock import patch

from utils import print_banner
from main import parse_args, run

class TestMain(unittest.TestCase):
    """Test case for the main module."""

    @patch('main.parse_args', return_value=argparse.Namespace(
        rating=None, state=None, reference=False, report=None,
        comment_hai=False, custom_field_hai=False, csv_output=False, verbose=False
    ))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main(self, mock_stdout, mock_args):
        """Test the main function."""
        try:
            run(mock_args)
        except Exception as e:
            self.fail(f"run() raised {type(e).__name__} unexpectedly!")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_banner(self, mock_stdout):
        """Test the print_banner function."""
        print_banner()
        output = mock_stdout.getvalue()
        self.assertIn(output, output)

    def test_parse_args(self):
        """Test the parse_args function."""
        sys.argv = ['main.py', '-r', 'none', '-s', 'new', '-i', '--report', '123', '-c', '-f', '-o', '-v']
        args = parse_args()
        self.assertEqual(args.rating, 'none')
        self.assertEqual(args.state, 'new')
        self.assertEqual(args.reference, True)
        self.assertEqual(args.report, ['123'])
        self.assertEqual(args.comment_hai, True)
        self.assertEqual(args.custom_field_hai, True)
        self.assertEqual(args.csv_output, True)
        self.assertEqual(args.verbose, True)

    @patch('sys.exit')
    @patch('argparse.ArgumentParser.print_help')
    def test_no_args(self, mock_print_help, mock_exit):
        """Test the parse_args function with no arguments."""
        sys.argv = ['main.py'] 
        parse_args()
        mock_print_help.assert_called_once()
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
