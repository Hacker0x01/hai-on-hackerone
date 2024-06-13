"""
Test module for the hai module.
"""
import asyncio
import unittest
from unittest.mock import MagicMock, patch

import pytest

from hai import (send_individual_prompt, send_to_hai,
                     wait_for_hai)

@patch('hai.aiohttp.ClientSession')
@patch('hai.wait_for_hai')
class TestSendIndividualPrompt:
    """
    Test case for the send_individual_prompt function.
    """
    @pytest.mark.asyncio
    async def test_send_individual_prompt(self, mock_wait_for_hai, mock_session):
        """
        Test case for the send_individual_prompt function.
        """
        mock_session.return_value.__aenter__.return_value.post.return_value.json = MagicMock()
        mock_wait_for_hai.return_value = {'state': 'completed'}

        report = '1'
        prompt = {
            "data": {
                "type": "completion-request",
                "attributes": {
                    "messages": "prompt",
                    "report_ids": [report]     
                }
            },
        }
        response = await send_individual_prompt(prompt, report, verbose=False)
        assert response['state'] == 'completed'
    @patch('builtins.print')
    @patch('hai.aiohttp.ClientSession')
    @patch('hai.wait_for_hai')
    @pytest.mark.asyncio
    async def test_send_individual_prompt_verbose(self, mock_print, mock_wait_for_hai, mock_session):
        """
        Test case for the send_individual_prompt function with verbose mode enabled.
        """
        mock_session.return_value.__aenter__.return_value.post.return_value.json = MagicMock()
        mock_wait_for_hai.return_value = {'state': 'completed'}

        report = '1'
        prompt = {
            "data": {
                "type": "completion-request",
                "attributes": {
                    "messages": "prompt",
                    "report_ids": [report]     
                }
            },
        }
        response = await send_individual_prompt(prompt, report, verbose=True)

        mock_print.assert_any_call("Request that is sent to Hai")
        assert response['state'] == 'completed'

class TestWaitForHai(unittest.TestCase):
    """
    Test case for the wait_for_hai function.
    """
    def test_wait_for_hai(self):
        """
        Test case for the wait_for_hai function.
        """
        response_data = {
            'data': {
                'attributes': {
                    'state': 'completed'
                }
            }
        }
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(wait_for_hai(response_data, verbose=False))
        self.assertEqual(response['state'], 'completed')

    def test_wait_for_hai_verbose(self):
        """
        Test case for the wait_for_hai function with verbose mode enabled.
        """
        response_data = {
            'data': {
                'attributes': {
                    'state': 'completed'
                }
            }
        }

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(wait_for_hai(response_data, verbose=True))
        self.assertEqual(response['state'], 'completed')

class TestSendToHai(unittest.TestCase):
    """
    Test case for the send_to_hai function.
    """
    @patch('hai.aiohttp.ClientSession')
    @patch('hai.wait_for_hai')
    @pytest.mark.asyncio
    async def test_send_to_hai(self, mock_wait_for_hai, mock_session):
        """
        Test case for the send_to_hai function.
        """
        mock_session.return_value.__aenter__.return_value.post.return_value.json = MagicMock()
        mock_wait_for_hai.return_value = {'state': 'completed'}

        report = '1'
        response = await send_to_hai(report, verbose=False)
        assert response['state'] == 'completed'

    @patch('hai.aiohttp.ClientSession')
    @patch('hai.wait_for_hai')
    @pytest.mark.asyncio
    async def test_send_to_hai_verbose(self, mock_wait_for_hai, mock_session):
        """
        Test case for the send_to_hai function with verbose mode enabled.
        """
        mock_session.return_value.__aenter__.return_value.post.return_value.json = MagicMock()
        mock_wait_for_hai.return_value = {'state': 'completed'}

        report = '1'
        response = await send_to_hai(report, verbose=True)
        assert response['state'] == 'completed'
