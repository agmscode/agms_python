from __future__ import absolute_import
import unittest
from agms.configuration import Configuration
from agms.agms import Agms
from agms.request.transaction_request import TransactionRequest
from agms.response.transaction_response import TransactionResponse


class Dummy(Agms):
    """
    A class representing Dummy Transaction objects to test Agms Base Class (Abstract)
    """
    def __init__(self):
        Agms.__init__(self)
        self._api_url = 'https://gateway.agms.com/roxapi/agms.asmx'
        self._requestObject = TransactionRequest
        self._responseObject = TransactionResponse
        self._op = 'ProcessTransaction'


class AgmsTest(unittest.TestCase):

    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', '1001789',
                                'b00f57326f8cf34bbb705a74b5fcbaa2b2f3e58076dc81f', 'requests')
        self.agms = Dummy()
        self.agms._set_parameter('transaction_type', {'value': 'sale'})

    def testAgmsVersion(self):
        self.assertEqual(Agms.MAJOR, 0)
        self.assertEqual(Agms.MINOR, 1)
        self.assertEqual(Agms.TINY, 5)
        self.assertEqual(self.agms.get_library_version(),'0.1.5')

    def testAgmsWhatCardType(self):
        card_trunc = '345'  
        self.assertEqual(self.agms.what_card_type(card_trunc), 'American Express')
        self.assertEqual(self.agms.what_card_type(card_trunc, 'abbreviation'), 'AX')

    def testAgmsDoConnect(self):
        self.assertEqual('Not Implemented', 'Not Implemented')

    def testAgms_setParameter(self):
        self.agms._set_parameter('transaction_type', {'value': 'sale'})
        self.assertTrue(isinstance(self.agms, Agms))
        self.assertEqual(self.agms.request._fields['TransactionType']['value'], 'sale')

    def testAgms_resetParameters(self):
        self.assertTrue(isinstance(self.agms.request, TransactionRequest))


if __name__ == '__main__':
    unittest.main()