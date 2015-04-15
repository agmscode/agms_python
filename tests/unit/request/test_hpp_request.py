from __future__ import absolute_import
import unittest
from agms.request.hpp_request import HPPRequest
from agms.request.request import Request


class HPPRequestTest(unittest.TestCase):

    def setUp(self):
        self.report_request = HPPRequest('ReturnHostedPaymentSetup')
        
    def testHPPClassAssignment(self):
        self.assertIsInstance(self.report_request, HPPRequest)
        self.assertIsInstance(self.report_request, Request)

    
if __name__ == '__main__':
    unittest.main()