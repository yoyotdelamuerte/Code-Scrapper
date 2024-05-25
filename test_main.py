import os
import unittest
from unittest.mock import patch, Mock

import requests

from main import get_html, save_to_file, extract_and_save_css, process_url


class TestWebScraper(unittest.TestCase):
    def test_get_html_success(self):
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.text = '<html><body>Hello, world!</body></html>'
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            html_content, error = get_html('https://example.com')
            self.assertIsNotNone(html_content)
            self.assertIsNone(error)

    def test_get_html_failure(self):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException('Mocked error')
            html_content, error = get_html('invalid-url')
            self.assertIsNone(html_content)
            self.assertIsNotNone(error)

    def test_save_to_file_success(self):
        content = 'Test content'
        file_name = 'test_file.txt'
        result = save_to_file(content, file_name)
        self.assertTrue(result.startswith('success'))
        self.assertTrue(os.path.exists(file_name))

    def test_save_to_file_failure(self):
        content = 'Test content'
        file_name = '/nonexistent/test_file.txt'
        result = save_to_file(content, file_name)
        self.assertTrue(result.startswith('error'))
        self.assertFalse(os.path.exists(file_name))

    def test_extract_and_save_css_success(self):
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.text = 'body { color: red; }'
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            soup = Mock()
            base_url = 'https://example.com'
            file_name = 'test_styles.css'
            result = extract_and_save_css(soup, base_url, file_name)
            self.assertTrue(result.startswith('success'))
            self.assertTrue(os.path.exists(file_name))

    def test_extract_and_save_css_failure(self):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException('Mocked error')
            soup = Mock()
            base_url = 'https://example.com'
            file_name = 'test_styles.css'
            result = extract_and_save_css(soup, base_url, file_name)
            self.assertTrue(result.startswith('error'))
            self.assertFalse(os.path.exists(file_name))



if __name__ == '__main__':
    unittest.main()
