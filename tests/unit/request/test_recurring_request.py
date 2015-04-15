from __future__ import absolute_import
import unittest
from agms.request.recurring_request import RecurringRequest
from agms.request.request import Request


class RecurringRequestTest(unittest.TestCase):

    def setUp(self):
        self.report_request = RecurringRequest('RecurringAdd')
        
    def testRecurringClassAssignment(self):
        self.assertIsInstance(self.report_request, RecurringRequest)
        self.assertIsInstance(self.report_request, Request)

    
if __name__ == '__main__':
    unittest.main()