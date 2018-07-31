import os
import mock
import unittest
from mock import patch
from ..jerakia import Jerakia

class JerakiaTestCase(unittest.TestCase):

    def setUp(self):
        self.jerakia = Jerakia(os.path.abspath('utils/jerakia.yaml'))
    
    def mocked_requests_get(self, *args, **kwargs):
        class MockResponse:
            text = ''
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
                MockResponse.text = str(json_data)

        return MockResponse({"found": "true","payload": "sto"}, 200)

    @mock.patch('jerakia.jerakia.requests.get', side_effect=mocked_requests_get)
    @mock.patch('jerakia.jerakia.json.loads', side_effect=(lambda x: x))
    def test_get_ok(self,mock_lookup,mock_json):
        """
        Test getting same dict response as expected from lookup
        """
        expected_dict = {
            "found": "true",
            "payload": "sto"
        }
        key='port'
        namespace=['common']
        response_dict = self.jerakia.lookup(key=key,namespace=namespace)
        # Check the contents of the response
        self.assertEqual(response_dict, expected_dict)