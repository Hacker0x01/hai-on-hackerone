"""
Tests for the reports module.
"""
import asyncio
import unittest
from unittest.mock import call, patch

from reports import (get_reports, load_api_variables, show_reports,
                         show_single_report)

class TestLoadApiVariables(unittest.TestCase):
    """
    Test case for the load_api_variables function.
    """
    @patch.dict('os.environ', {
        'API_NAME': 'test_name',
        'API_KEY': 'test_key',
        'PROGRAM_HANDLE': 'test_handle',
    })
    def test_load_api_variables(self):
        """
        Test case for the load_api_variables function.
        """
        api_name, api_key, program_handle, headers = load_api_variables()

        self.assertEqual(api_name, 'test_name')
        self.assertEqual(api_key, 'test_key')
        self.assertEqual(program_handle, 'test_handle')
        self.assertEqual(headers, {'Accept': 'application/json'})

class TestReports(unittest.TestCase):
    """
    Test case for the reports module.
    """
    @patch('reports.requests.get')
    @patch('reports.send_to_hai')
    @patch('reports.hai_actions')
    def test_get_reports(self, mock_hai_actions, mock_send_to_hai, mock_get):
        """
        Test the get_reports function.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": {
                "id": "1",
                "attributes": {"title": "Test Report", "state": "new"}
            },
            "links": {"next": None} 
        }
        mock_send_to_hai.return_value = (None, None, None, None, None, None, None, None, None, None)
        mock_hai_actions.return_value = None
        asyncio.run(get_reports(['1'], 'low', 'new', False, False, False, False))
        self.assertEqual(mock_get.call_count, 1)
        mock_send_to_hai.assert_called_once()
        mock_hai_actions.assert_called_once()

# WIP
# class TestGetAllReports(unittest.IsolatedAsyncioTestCase):
#     def test_get_all_reports(self, mock_show_reports):

class TestShowReports(unittest.IsolatedAsyncioTestCase):
    """
    Test case for the show_reports function.
    """
    @patch('reports.show_single_report')
    @patch('reports.send_to_hai')
    @patch('reports.hai_actions')
    async def test_show_reports(self, mock_hai_actions, mock_send_to_hai, mock_show_single_report):
        """
        Test the show_reports function.
        """
        response = {
            "data": [
                {
                    "id": "1",
                    "attributes": {"title": "Test Report 1", "state": "new"}
                },
                {
                    "id": "2",
                    "attributes": {"title": "Test Report 2", "state": "closed"}
                }
            ]
        }
        mock_send_to_hai.return_value = (None, None, None, None, None, None, None, None, None, None)
        mock_hai_actions.return_value = None
        await show_reports(response, False, False, False, False)
        self.assertEqual(mock_show_single_report.call_count, 2)
        self.assertEqual(mock_send_to_hai.call_args_list, [call("1", False), call("2", False)])
        self.assertEqual(mock_hai_actions.call_args_list, [call(None, None, None, None, None, None, None, None, None, None, '1', False, False, False, False), call(None, None, None, None, None, None, None, None, None, None, '2', False, False, False, False)])

class TestShowSingleReport(unittest.TestCase):
    """
    Test case for the show_single_report function.
    """
    @patch('builtins.print')
    def test_show_single_report(self, mock_print):
        """
        Test the show_single_report function.
        """
        report = {
            "data": {
                "id": "1",
                "attributes": {
                    "title": "Test Report",
                    "state": "new"
                }
            }
        }

        show_single_report(report)
        mock_print.assert_any_call("_____________")
        mock_print.assert_any_call("Report ID: 1")
        mock_print.assert_any_call("Report Title: Test Report")
        mock_print.assert_any_call("Report State: new")
        mock_print.assert_any_call("Reporter Reputation: N/A")
        mock_print.assert_any_call("Reporter Signal: N/A")

    @patch('builtins.print')
    def test_show_single_report_with_reporter_data(self, mock_print):
        """
        Test the show_single_report function with reporter data.
        """
        report = {
            "data": {
                "id": "1",
                "attributes": {
                    "title": "Test Report",
                    "state": "new"
                },
                "relationships": {
                    "reporter": {
                        "data": {
                            "attributes": {
                                "reputation": 100,
                                "signal": 50
                            }
                        }
                    }
                }
            }
        }
        show_single_report(report)
        mock_print.assert_any_call("Reporter Reputation: 100")
        mock_print.assert_any_call("Reporter Signal: 50")

    @patch('builtins.print')
    def test_show_single_report_with_reporter_data_missing_reputation(self, mock_print):
        """
        Test the show_single_report function with reporter data missing reputation.
        """
        report = {
            "data": {
                "id": "1",
                "attributes": {
                    "title": "Test Report",
                    "state": "new"
                },
                "relationships": {
                    "reporter": {
                        "data": {
                            "attributes": {
                                "signal": 50
                            }
                        }
                    }
                }
            }
        }
        show_single_report(report)
        mock_print.assert_any_call("Reporter Reputation: N/A")
        mock_print.assert_any_call("Reporter Signal: 50")

    @patch('builtins.print')
    def test_show_single_report_with_reporter_data_missing_signal(self, mock_print):
        """
        Test the show_single_report function with reporter data missing signal.
        """
        report = {
            "data": {
                "id": "1",
                "attributes": {
                    "title": "Test Report",
                    "state": "new"
                },
                "relationships": {
                    "reporter": {
                        "data": {
                            "attributes": {
                                "reputation": 100
                            }
                        }
                    }
                }
            }
        }
        show_single_report(report)
        mock_print.assert_any_call("Reporter Reputation: 100")
        mock_print.assert_any_call("Reporter Signal: N/A")
