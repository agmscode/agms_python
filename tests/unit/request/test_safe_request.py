from __future__ import absolute_import
import unittest
from agms.request.safe_request import SAFERequest
from agms.request.request import Request


class SAFERequestTest(unittest.TestCase):

    def setUp(self):
        self.safe_request = SAFERequest('AddToSAFE')
        
    def testSAFEClassAssignment(self):
        self.assertIsInstance(self.safe_request, SAFERequest)
        self.assertIsInstance(self.safe_request, Request)

    
if __name__ == '__main__':
    unittest.main()