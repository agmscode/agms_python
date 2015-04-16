from __future__ import absolute_import
import unittest
from agms.request.report_request import ReportRequest
from agms.request.request import Request


class ReportRequestTest(unittest.TestCase):

    def setUp(self):
        self.report_request = ReportRequest('TransactionAPI')
        
    def testReportClassAssignment(self):
        self.assertTrue(isinstance(self.report_request, ReportRequest))
        self.assertTrue(isinstance(self.report_request, Request))

    
if __name__ == '__main__':
    unittest.main()