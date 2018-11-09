import shutil, tempfile
from os import path
import sys
import yaml
import unittest
import mock
import msgpack
import jerakia
from jerakia import render


class TestClient(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.default_config = dict(
                protocol = 'http',
                host = 'localhost',
                port = 9843,
                version = 1,
                token = 'ansible:4142672cd08d4dbb9eb3c1234567e46c1b85b20d75501ebc319c17a62dae636c1509b8bea1a66b3e',
        )
        self.file_config = dict(
                protocol = 'https',
                host = 'test.example.com',
                port = 1234,
                version = 9999,
                token = 'ansible:4142672cd08d4dbb9eb3c1234567e46c1b85b20d75501ebc319c17a62dae636c1509b8bea1a66b3e',
        )
        self.render_file = dict(
                fieldA = '{{retrieveJerakia(it)}}',
                fieldB = 'test',
        )
        self.token = 'ansible:4142672cd08d4dbb9eb3c1234567e46c1b85b20d75501ebc319c17a62dae636c1509b8bea1a66b3e'

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_default_config(self):
        instance = jerakia.Client(self.token)
        self.assertIsNotNone(instance.config)
        for key in self.default_config.keys():
            self.assertEqual(instance.config[key], self.default_config[key])

    def test_fromfile_config(self):
        config_file_path = path.join(self.test_dir, 'jerakia_config.yml')
        with open(config_file_path, 'w') as outfile:
            yaml.dump(self.file_config, outfile, default_flow_style=False)

        instance = jerakia.Client.fromfile(config_file_path)
        self.assertIsNotNone(instance.config)
        for key in self.default_config.keys():
            self.assertEqual(instance.config[key], self.file_config[key])

    def mocked_requests_get_json(self, *args, **kwargs):
        """
        Mock response of requests.get using JSON
        """
        class MockResponseJson:
            def __init__(self, data, status_code, response_type):
                self.data = data
                self.headers = { "content-type": response_type, 'status_code': status_code }
            def json(self):
                return self.data
            def raise_for_status(self):
                return self.headers['status_code']

        return MockResponseJson({"found": "true","payload": "sesame"}, 200,'application/json')

    @mock.patch('jerakia.client.requests.get', side_effect=mocked_requests_get_json)
    def test_lookup_json(self,mock_lookup):
        """
        Test getting same dict response as expected from lookup using JSON
        """
        instance = jerakia.Client(token=self.token)
        expected_dict = {
            "found": "true",
            "payload": "sesame"
        }
        response_dict = instance.lookup(key='open',namespace='common',content_type='json')
        # Check the contents of the response
        self.assertEqual(response_dict, expected_dict)

    def mocked_requests_get_msgpack(self, *args, **kwargs):
        """
        Mock response of requests.get using msgpack
        """
        class MockResponseMsgpack:
            content = ''
            def __init__(self, data, status_code, response_type):
                self.data = data
                self.headers = { 'content-type': response_type, 'status_code': status_code }
                MockResponseMsgpack.content = data
            def raise_for_status(self):
                return self.headers['status_code']

        return MockResponseMsgpack(msgpack.packb({"found": "true","payload": "sesame"}, use_bin_type=True), 200,'application/x-msgpack')

    @mock.patch('jerakia.client.requests.get', side_effect=mocked_requests_get_msgpack)
    def test_lookup_msgpack(self,mock_lookup):
        """
        Test getting same dict response as expected from lookup using JSON
        """
        instance = jerakia.Client(token=self.token)
        expected_dict = {
            "found": "true",
            "payload": "sesame"
        }
        response_dict = instance.lookup(key='open',namespace='common',content_type='msgpack')
        # Check the contents of the response
        self.assertEqual(response_dict, expected_dict)

    @mock.patch('jerakia.client.requests.get', side_effect=mocked_requests_get_json)
    def test_render_json(self,mock_lookup):
        """
        Test render occurs successfully
        """
        config_file_path = path.join(self.test_dir, 'render_file.yml')
        with open(config_file_path, 'w') as outfile:
            yaml.dump(self.render_file, outfile, default_flow_style=True)

        instance = jerakia.Client(token=self.token)

        fields = {'it': 'common/test'}
        if 'it' in fields:
            test_out = render.render(template_path=config_file_path, jerakia_instance=instance, metadata_dict=dict(env='dev'), data=fields)
            self.assertIsNotNone(test_out)
            expected_test_out = '{' + "fieldA: 'sesame'" + ', ' + "fieldB: test" + '}'+ '\n'
            self.assertEqual(test_out, expected_test_out)

if __name__ == '__main__':
    unittest.main()
