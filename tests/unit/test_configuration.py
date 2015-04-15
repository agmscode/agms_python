from __future__ import absolute_import
import unittest
from agms.configuration import Configuration
from agms.util.requests_client import RequestsClient


class AgmsTest(unittest.TestCase):

    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', '1001789',
                                'b00f57326f8cf34bbb705a74b5fcbaa2b2f3e58076dc81f', 'requests')
        self.config = Configuration.instantiate()

    def testConfigurationInit(self):
        self.assertEqual(Configuration.gateway_username, 'agmsdevdemo')
        self.assertEqual(Configuration.gateway_account, '1001789')
        self.assertEqual(Configuration.gateway_api_key, 'b00f57326f8cf34bbb705a74b5fcbaa2b2f3e58076dc81f')

    def testConfigurationInstantiate(self):
        self.assertEqual(self.config.gateway_username, 'agmsdevdemo')
        self.assertEqual(self.config.gateway_account, '1001789')
        self.assertEqual(self.config.gateway_api_key, 'b00f57326f8cf34bbb705a74b5fcbaa2b2f3e58076dc81f')

    def testHttpClient(self):
        self.assertIsInstance(self.config._http_client, RequestsClient)


if __name__ == '__main__':
    unittest.main()