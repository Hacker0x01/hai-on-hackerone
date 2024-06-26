"""Test cases for the file watcher module."""
import unittest
from unittest.mock import patch, mock_open, MagicMock
import asyncio
from threading import Lock
import sys

from watch_reports import (
    get_line_count,
    process_new_lines,
    run_python_tool,
    FileChangeHandler,
    monitor_file,
    FILE_TO_WATCH,
    line_count_lock
)

# Mock imports from cli/actions.py and cli/hai.py
# sys.path.append('/hai-on-hackerone/cli/')
sys.path.append('/hai-on-hackerone/watcher/')

class TestWatchReports(unittest.TestCase):
    """Test case for the watch_reports module."""

    @patch('builtins.open', new_callable=mock_open, read_data="line1\nline2\n")
    def test_get_line_count(self, mock_file):
        """Test get_line_count function."""
        filepath = 'dummy_path'
        count = get_line_count(filepath)
        self.assertEqual(count, 2)
        mock_file.assert_called_once_with(filepath, 'r', encoding='UTF-8')

    @patch('builtins.open', new_callable=mock_open, read_data="line1\nline2\nline3\n")
    @patch('watch_reports.run_python_tool', new_callable=MagicMock)
    def test_process_new_lines(self, mock_run_python_tool, mock_file):
        """Test process_new_lines function."""
        filepath = 'dummy_path'
        initial_count = 1
        new_count = process_new_lines(filepath, initial_count)
        self.assertEqual(new_count, 3)
        self.assertEqual(mock_run_python_tool.call_count, 2)
        mock_run_python_tool.assert_any_await("line2")
        mock_run_python_tool.assert_any_await("line3")

    @patch('watch_reports.send_to_hai', new_callable=MagicMock)
    @patch('watch_reports.hai_actions', new_callable=MagicMock)
    def test_run_python_tool(self, mock_hai_actions, mock_send_to_hai):
        """Test run_python_tool function."""
        mock_send_to_hai.return_value = asyncio.Future()
        mock_send_to_hai.return_value.set_result((
            'valid', 0.9, 'reasoning', 'complex', 0.8, 'reasoning',
            0.7, 'reasoning', 'area', 'owner'
        ))
        report_number = "123"
        asyncio.run(run_python_tool(report_number))
        mock_send_to_hai.assert_awaited_once_with(report_number, True)
        mock_hai_actions.assert_called_once()

    @patch('watch_reports.process_new_lines', new_callable=MagicMock)
    @patch('watch_reports.line_count_lock', new_callable=Lock)
    def test_on_modified(self, mock_line_count_lock, mock_process_new_lines):
        """Test on_modified method in FileChangeHandler."""
        handler = FileChangeHandler(FILE_TO_WATCH)
        event = MagicMock()
        event.src_path = FILE_TO_WATCH
        handler.on_modified(event)
        mock_process_new_lines.assert_called_once_with(FILE_TO_WATCH, handler.initial_line_count)

    @patch('watch_reports.Observer')
    @patch('watch_reports.FileChangeHandler')
    def test_monitor_file(self, mock_file_change_handler, mock_observer):
        """Test monitor_file function."""
        mock_handler_instance = mock_file_change_handler.return_value
        mock_observer_instance = mock_observer.return_value

        with patch('watch_reports.Observer.start', return_value=None):
            with patch('watch_reports.Observer.join', return_value=None):
                with patch('watch_reports.Observer.stop', return_value=None):
                    monitor_file(FILE_TO_WATCH)

        mock_file_change_handler.assert_called_once_with(FILE_TO_WATCH)
        mock_observer_instance.schedule.assert_called_once_with(
            mock_handler_instance, path=FILE_TO_WATCH, recursive=False)
        mock_observer_instance.start.assert_called_once()
        mock_observer_instance.join.assert_called_once()