#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import httpretty
import unittest
from agms.configuration import Configuration
from agms.transaction import Transaction


class TransactionTest(unittest.TestCase):

    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', '1001789', 'b00f57326f8cf34bbb705a74b5fcbaa2b2f3e58076dc81f', 'pycurl')
        self.transaction = Transaction()
        
    def testTransactionClassAssignment(self):
        self.assertTrue(isinstance(self.transaction, Transaction))

    def testTransactionOp(self):
        self.assertEqual(self.transaction._op, 'ProcessTransaction')

    @httpretty.activate
    def testTransactionProcess(self):
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
        self.assertTrue(isinstance(self.transaction.response.to_array(), dict))

    @httpretty.activate
    def testSuccessfulSale(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_sale_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'sale'},
            'amount': {'value': '10.00'}, 
            'cc_number': {'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')
        self.assertEqual(self.transaction_result['transaction_id'], '549865')

    @httpretty.activate
    def testFailedSale(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.failed_sale_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'sale'},
            'amount': {'value': '10.00'}, 
            'cc_number': {'value': '4111111111111111'},
            'cc_exp_date': {'value': '0514'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Declined')
        self.assertEqual(self.transaction_result['response_code'], '2')
        self.assertEqual(self.transaction_result['transaction_id'], '549879')

    @httpretty.activate
    def testSuccessfulAuthorize(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_authorize_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'auth'},
            'amount': {'value': '10.00'}, 
            'cc_number': {'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')
        self.assertEqual(self.transaction_result['transaction_id'], '550945')

    @httpretty.activate
    def testFailedAuthorize(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.failed_authorize_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'auth'},
            'amount': {'value': '10.00'}, 
            'cc_number': {'value': '4111111111111111'},
            'cc_exp_date': {'value': '0514'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Declined')
        self.assertEqual(self.transaction_result['response_code'], '2')
        self.assertEqual(self.transaction_result['transaction_id'], '550941')

    @httpretty.activate
    def testSuccessfulCapture(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_authorize_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'auth'},
            'amount': {'value': '10.00'}, 
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

        transaction_id = self.transaction_result['transaction_id']

        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_capture_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'capture'},
            'transaction_id': {'value': transaction_id},
            'amount': {'value': '10'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Capture successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')
        self.assertEqual(self.transaction_result['transaction_id'], '550946')

    @httpretty.activate
    def testPartialCapture(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_authorize_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'auth'},
            'amount': {'value': '10.00'}, 
            'cc_number': {'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

        transaction_id = self.transaction_result['transaction_id']

        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.partial_capture_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'capture'},
            'transaction_id': {'value': transaction_id},
            'amount': {'value': '5'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Capture successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')
        self.assertEqual(self.transaction_result['transaction_id'], '550946')

    @httpretty.activate
    def testFailedCapture(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_authorize_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'auth'},
            'amount': {'value': '10.00'}, 
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.failed_capture_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'capture'},
            'transaction_id': {'value': '123'},
            'amount': {'value': '0.01'}
        }
        try:
            self.transaction_result = self.transaction.process(params)
        except Exception as err:
            self.assertEqual(err.args[1]['response_code'], '10')
            self.assertEqual(err.args[1]['response_message'], 'Transaction ID is not valid. Please double check your Transaction ID')
            self.assertEqual(err.args[1]['transaction_id'], '550949')

    @httpretty.activate
    def testSuccessfulRefund(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_sale_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'sale'},
            'amount': {'value': '10.00'}, 
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

        transaction_id = self.transaction_result['transaction_id']

        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_refund_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'refund'},
            'transaction_id': {'value': transaction_id},
            'amount': {'value': '10'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'refund successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')
        self.assertEqual(self.transaction_result['transaction_id'], '550946')

    @httpretty.activate
    def testPartialRefund(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_sale_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'sale'},
            'amount': {'value': '10.00'}, 
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

        transaction_id = self.transaction_result['transaction_id']

        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.partial_refund_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'refund'},
            'transaction_id': {'value': transaction_id},
            'amount': {'value': '5'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'refund successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')
        self.assertEqual(self.transaction_result['transaction_id'], '550946')

    @httpretty.activate
    def testFailedRefund(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_sale_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'sale'},
            'amount': {'value': '10.00'}, 
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.failed_refund_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'refund'},
            'transaction_id': {'value': '123'},
            'amount': {'value': '20'}
        }
        try:
            self.transaction_result = self.transaction.process(params)
        except Exception as err:
            self.assertEqual(err.args[1]['response_code'], '10')
            self.assertEqual(err.args[1]['response_message'], 'Transaction ID is not valid. Please double check your Transaction ID')
            self.assertEqual(err.args[1]['transaction_id'], '550953')

    @httpretty.activate
    def testSuccessfulVoid(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_sale_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'sale'},
            'amount': {'value': '10.00'}, 
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

        transaction_id = self.transaction_result['transaction_id']

        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_void_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'void'},
            'transaction_id': {'value': transaction_id}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'void successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')
        self.assertEqual(self.transaction_result['transaction_id'], '550946')
        
    @httpretty.activate
    def testFailedVoid(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_sale_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'sale'},
            'amount': {'value': '10.00'}, 
            'cc_number': {'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.failed_void_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'void'},
            'transaction_id': {'value': '123'}
        }
        try:
            self.transaction_result = self.transaction.process(params)
        except Exception as err:
            self.assertEqual(err.args[1]['response_code'], '10')
            self.assertEqual(err.args[1]['response_message'], 'Transaction ID is not valid. Please double check your Transaction ID')
            self.assertEqual(err.args[1]['transaction_id'], '550953')

    @httpretty.activate
    def testSuccessfulVerify(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_authorize_response(),
                                content_type="application/xml")
        params = {
            'transaction_type': {'value': 'auth'},
            'amount': {'value': '1.00'}, 
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

        transaction_id = self.transaction_result['transaction_id']

        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_void_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'void'},
            'transaction_id': {'value': transaction_id}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'void successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')
        self.assertEqual(self.transaction_result['transaction_id'], '550946')

    @httpretty.activate
    def testFailedVerify(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.successful_authorize_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'auth'},
            'amount': {'value': '1.00'}, 
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/agms.asmx",
                                body=self.failed_void_response(),
                                content_type="application/xml")

        params = {
            'transaction_type': {'value': 'void'},
            'transaction_id': {'value': '123'}
        }
        try:
            self.transaction_result = self.transaction.process(params)
        except Exception as err:
            self.assertEqual(err.args[1]['response_code'], '10')
            self.assertEqual(err.args[1]['response_message'], 'Transaction ID is not valid. Please double check your Transaction ID')
            self.assertEqual(err.args[1]['transaction_id'], '550953')


    def successful_sale_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ProcessTransactionResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ProcessTransactionResult><STATUS_CODE>1</STATUS_CODE><STATUS_MSG>Approved</STATUS_MSG><TRANS_ID>549865</TRANS_ID><AUTH_CODE>9999</AUTH_CODE><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID>652</MERCHANT_ID><CUSTOMER_MESSAGE /><RRN /></ProcessTransactionResult></ProcessTransactionResponse></soap:Body></soap:Envelope>
            """

    def failed_sale_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ProcessTransactionResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ProcessTransactionResult><STATUS_CODE>2</STATUS_CODE><STATUS_MSG>Declined</STATUS_MSG><TRANS_ID>549879</TRANS_ID><AUTH_CODE>1234</AUTH_CODE><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID>652</MERCHANT_ID><CUSTOMER_MESSAGE /><RRN /></ProcessTransactionResult></ProcessTransactionResponse></soap:Body></soap:Envelope>
            """

    def successful_authorize_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ProcessTransactionResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ProcessTransactionResult><STATUS_CODE>1</STATUS_CODE><STATUS_MSG>Approved</STATUS_MSG><TRANS_ID>550945</TRANS_ID><AUTH_CODE>9999</AUTH_CODE><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID>652</MERCHANT_ID><CUSTOMER_MESSAGE /><RRN /></ProcessTransactionResult></ProcessTransactionResponse></soap:Body></soap:Envelope>
            """

    def failed_authorize_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ProcessTransactionResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ProcessTransactionResult><STATUS_CODE>2</STATUS_CODE><STATUS_MSG>Declined</STATUS_MSG><TRANS_ID>550941</TRANS_ID><AUTH_CODE>1234</AUTH_CODE><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID>652</MERCHANT_ID><CUSTOMER_MESSAGE /><RRN /></ProcessTransactionResult></ProcessTransactionResponse></soap:Body></soap:Envelope>
            """

    def successful_capture_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ProcessTransactionResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ProcessTransactionResult><STATUS_CODE>1</STATUS_CODE><STATUS_MSG>Capture successful: Approved</STATUS_MSG><TRANS_ID>550946</TRANS_ID><AUTH_CODE>9999</AUTH_CODE><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID>652</MERCHANT_ID><CUSTOMER_MESSAGE /><RRN /></ProcessTransactionResult></ProcessTransactionResponse></soap:Body></soap:Envelope>
            """

    def partial_capture_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ProcessTransactionResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ProcessTransactionResult><STATUS_CODE>1</STATUS_CODE><STATUS_MSG>Capture successful: Approved</STATUS_MSG><TRANS_ID>550946</TRANS_ID><AUTH_CODE>9999</AUTH_CODE><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID>652</MERCHANT_ID><CUSTOMER_MESSAGE /><RRN /></ProcessTransactionResult></ProcessTransactionResponse></soap:Body></soap:Envelope>
            """

    def failed_capture_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ProcessTransactionResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ProcessTransactionResult><STATUS_CODE>10</STATUS_CODE><STATUS_MSG>Transaction ID is not valid. Please double check your Transaction ID</STATUS_MSG><TRANS_ID>550949</TRANS_ID><AUTH_CODE /><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID>652</MERCHANT_ID><CUSTOMER_MESSAGE /><RRN /></ProcessTransactionResult></ProcessTransactionResponse></soap:Body></soap:Envelope>
            """

    def successful_refund_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ProcessTransactionResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ProcessTransactionResult><STATUS_CODE>1</STATUS_CODE><STATUS_MSG>refund successful: Approved</STATUS_MSG><TRANS_ID>550946</TRANS_ID><AUTH_CODE>9999</AUTH_CODE><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID>652</MERCHANT_ID><CUSTOMER_MESSAGE /><RRN /></ProcessTransactionResult></ProcessTransactionResponse></soap:Body></soap:Envelope>
            """

    def partial_refund_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ProcessTransactionResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ProcessTransactionResult><STATUS_CODE>1</STATUS_CODE><STATUS_MSG>refund successful: Approved</STATUS_MSG><TRANS_ID>550946</TRANS_ID><AUTH_CODE>9999</AUTH_CODE><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID>652</MERCHANT_ID><CUSTOMER_MESSAGE /><RRN /></ProcessTransactionResult></ProcessTransactionResponse></soap:Body></soap:Envelope>
            """

    def failed_refund_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ProcessTransactionResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ProcessTransactionResult><STATUS_CODE>10</STATUS_CODE><STATUS_MSG>Transaction ID is not valid. Please double check your Transaction ID</STATUS_MSG><TRANS_ID>550953</TRANS_ID><AUTH_CODE /><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID>652</MERCHANT_ID><CUSTOMER_MESSAGE /><RRN /></ProcessTransactionResult></ProcessTransactionResponse></soap:Body></soap:Envelope>
            """

    def successful_void_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ProcessTransactionResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ProcessTransactionResult><STATUS_CODE>1</STATUS_CODE><STATUS_MSG>void successful: Approved</STATUS_MSG><TRANS_ID>550946</TRANS_ID><AUTH_CODE>9999</AUTH_CODE><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID>652</MERCHANT_ID><CUSTOMER_MESSAGE /><RRN /></ProcessTransactionResult></ProcessTransactionResponse></soap:Body></soap:Envelope>
            """

    def failed_void_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><ProcessTransactionResponse xmlns=\"https://gateway.agms.com/roxapi/\"><ProcessTransactionResult><STATUS_CODE>10</STATUS_CODE><STATUS_MSG>Transaction ID is not valid. Please double check your Transaction ID</STATUS_MSG><TRANS_ID>550953</TRANS_ID><AUTH_CODE /><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID>652</MERCHANT_ID><CUSTOMER_MESSAGE /><RRN /></ProcessTransactionResult></ProcessTransactionResponse></soap:Body></soap:Envelope>
            """


if __name__ == '__main__':
    unittest.main()