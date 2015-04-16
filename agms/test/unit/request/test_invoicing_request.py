from __future__ import absolute_import
import unittest
from agms.request.invoicing_request import InvoicingRequest
from agms.request.request import Request


class InvoicingRequestTest(unittest.TestCase):

    def setUp(self):
        self.report_request = InvoicingRequest('RetrieveCustomerIDList')
        
    def testInvoicingClassAssignment(self):
        self.assertTrue(isinstance(self.report_request, InvoicingRequest))
        self.assertTrue(isinstance(self.report_request, Request))

    
if __name__ == '__main__':
    unittest.main()