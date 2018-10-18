import shutil, tempfile
from os import path
import yaml
import unittest
import mock
from jerakia.jerakia import Jerakia

class TestJerakia(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.default_config = dict(
                protocol = 'http',
                host = 'localhost',
                port = 9843,
                version = 1)
        self.file_config = dict(
                protocol = 'https',
                host = 'test.example.com',
                port = 1234,
                version = 9999,
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_default_config(self):
        instance = Jerakia()
        self.assertIsNotNone(instance.config)
        for key in self.default_config.keys():
            self.assertEqual(instance.config[key], self.default_config[key])

    def test_fromfile_config(self):
        config_file_path = path.join(self.test_dir, 'jerakia_config.yml')
        with open(config_file_path, 'w') as outfile:
            yaml.dump(self.file_config, outfile, default_flow_style=False)

        instance = Jerakia.fromfile(config_file_path)
        self.assertIsNotNone(instance.config)
        for key in self.default_config.keys():
            self.assertEqual(instance.config[key], self.file_config[key])

    def mocked_requests_get(self, *args, **kwargs):
        """
        Mock response of requests.get
        """
        class MockResponse:
            text = ''
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
                MockResponse.text = json_data

        return MockResponse({"found": "true","payload": "sesame"}, 200)

    @mock.patch('jerakia.jerakia.requests.get', side_effect=mocked_requests_get)
    def test_lookup(self,mock_lookup):
        """
        Test getting same dict response as expected from lookup
        """
        instance = Jerakia()
        expected_dict = {
            "found": "true",
            "payload": "sesame"
        }
        response_dict = instance.lookup(key='open',namespace='common')
        # Check the contents of the response
        self.assertEqual(response_dict, expected_dict)

if __name__ == '__main__':
    unittest.main()
