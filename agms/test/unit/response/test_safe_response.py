#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import httpretty
import unittest
from agms.configuration import Configuration
from agms.safe import SAFE
from agms.response.safe_response import SAFEResponse
from agms.response.response import Response


class SAFEResponseTest(unittest.TestCase):

    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', '1001789', 'b00f57326f8cf34bbb705a74b5fcbaa2b2f3e58076dc81f', 'requests')
        self.safe = SAFE()


    @httpretty.activate
    def testSAFEClassAssignment(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/AGMS_SAFE_API.asmx",
                                body=self.successful_SAFEAdd_response(),
                                content_type="application/xml")
        params = {
            'payment_type': {'value': 'creditcard'},
            'first_name': {'value': 'Joe'},
            'last_name': {'value': 'Smith'},
            'cc_number': {'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.safe_response = self.safe.add(params)
        self.assertTrue(isinstance(self.safe.response, SAFEResponse))
        self.assertTrue(isinstance(self.safe.response, Response))

    def successful_SAFEAdd_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><AddToSAFEResponse xmlns=\"https://gateway.agms.com/roxapi/\"><AddToSAFEResult><STATUS_CODE>1</STATUS_CODE><STATUS_MSG>SAFE Record added successfully. No transaction processed.</STATUS_MSG><TRANS_ID /><AUTH_CODE /><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID>1035593</SAFE_ID><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID /><CUSTOMER_MESSAGE /><RRN /></AddToSAFEResult></AddToSAFEResponse></soap:Body></soap:Envelope>
            """

if __name__ == '__main__':
    unittest.main()