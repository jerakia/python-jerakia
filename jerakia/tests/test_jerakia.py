import shutil, tempfile
from os import path
import yaml
import unittest
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


if __name__ == '__main__':
    unittest.main()
