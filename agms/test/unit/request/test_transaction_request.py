from __future__ import absolute_import
import unittest
from agms.request.transaction_request import TransactionRequest
from agms.request.request import Request


class TransactionRequestTest(unittest.TestCase):

    def setUp(self):
        self.transaction_request = TransactionRequest('ProcessTransaction')
        
    def testTransactionClassAssignment(self):
        self.assertTrue(isinstance(self.transaction_request, TransactionRequest))
        self.assertTrue(isinstance(self.transaction_request, Request))

    
if __name__ == '__main__':
    unittest.main()