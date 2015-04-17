#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import httpretty
import unittest
from agms.configuration import Configuration
from agms.transaction import Transaction
from agms.response.transaction_response import TransactionResponse
from agms.response.response import Response


class TransactionResponseTest(unittest.TestCase):
    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', '1001789', 'b00f57326f8cf34bbb705a74b5fcbaa2b2f3e58076dc81f', 'pycurl')
        self.transaction = Transaction()


    @httpretty.activate
    def testTransactionClassAssignment(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_sale_response(),
                                content_type="application/xml")
        params = {
            'transaction_type': {'value': 'sale'},
            'amount': {'value': '100.00'},
            'cc_number': {'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertTrue(isinstance(self.transaction.response, TransactionResponse))
        self.assertTrue(isinstance(self.transaction.response, Response))

    def successful_sale_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ProcessTransactionResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ProcessTransactionResult><STATUS_CODE>1</STATUS_CODE><STATUS_MSG>Approved</STATUS_MSG><TRANS_ID>549865</TRANS_ID><AUTH_CODE>9999</AUTH_CODE><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID>652</MERCHANT_ID><CUSTOMER_MESSAGE /><RRN /></ProcessTransactionResult></ProcessTransactionResponse></soap:Body></soap:Envelope>
            """
if __name__ == '__main__':
    unittest.main()