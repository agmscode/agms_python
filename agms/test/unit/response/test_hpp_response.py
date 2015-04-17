#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import httpretty
import unittest
from agms.configuration import Configuration
from agms.hpp import HPP
from agms.response.hpp_response import HPPResponse
from agms.response.response import Response


class HPPResponseTest(unittest.TestCase):

    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', '1001789', 'b00f57326f8cf34bbb705a74b5fcbaa2b2f3e58076dc81f', 'pycurl')
        self.hpp = HPP()

    @httpretty.activate
    def testHPPClassAssignment(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/AGMS_HostedPayment.asmx",
                                body=self.successful_HPPGetHash_response(),
                                content_type="application/xml")
        params = {
            'transaction_type': {'value': 'sale'},
            'amount': {'value': '20.00'},
            'first_name': {'setting': 'required'},
            'last_name': {'setting': 'required'},
            'zip': {'setting': 'required'},
            'email': {'setting': 'required'},
            'hpp_format': {'value': '1'},
        }
        self.hpp.generate(params)
        self.assertTrue(isinstance(self.hpp.response, HPPResponse))
        self.assertTrue(isinstance(self.hpp.response, Response))

    def successful_HPPGetHash_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ReturnHostedPaymentSetupResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ReturnHostedPaymentSetupResult>wZZaqjttCWc9oy/hby3pD7IwYzLJ3oSo80HFylbOJkQ%3D</ReturnHostedPaymentSetupResult></ReturnHostedPaymentSetupResponse></soap:Body></soap:Envelope>
            """

if __name__ == '__main__':
    unittest.main()