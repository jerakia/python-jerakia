import os
import mock
import unittest
from mock import patch
from ..jerakia import Jerakia

class JerakiaTestCase(unittest.TestCase):

    def setUp(self):
        self.jerakia = Jerakia(os.path.abspath('utils/jerakia.yaml'))

    @mock.patch('jerakia.jerakia.requests.get')
    def test_get_ok(self, mock_lookup):
        """
        Test getting a 200 OK response from the lookup method of Jerakia.
        """
        # Construct mock response object
        mock_response = mock.Mock()
        expected_dict = {
            "ports": [
                "80",
                "443",
            ]
        }

        mock_response.json.return_value = expected_dict

        # Assign our mock response as the result of patched function
        mock_lookup.return_value = mock_response
        key='port'
        namespace='common'
        response_dict = self.jerakia.rawlookup(key=key,namespace=namespace)
    
        # Check that our function made the expected internal calls
        mock_lookup.assert_called_once_with(key=key,namespace=namespace)
        self.assertEqual(1, mock_response.json.call_count)

        # Check the contents of the response
        self.assertEqual(response_dict, expected_dict)