from __future__ import absolute_import
import httpretty
import unittest
from agms.configuration import Configuration
from agms.safe import SAFE
from agms.exception.response_exception import ResponseException


class SAFETest(unittest.TestCase):

    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', '1001789', 'b00f57326f8cf34bbb705a74b5fcbaa2b2f3e58076dc81f', 'requests')
        self.safe = SAFE()
        
    def testSAFEClassAssignment(self):
        self.assertIsInstance(self.safe, SAFE)

    @httpretty.activate
    def testSuccessfulSAFEAdd(self):
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
        self.safe_result = self.safe.add(params)
        self.assertEqual(self.safe.response.is_successful(), True)
        self.assertEqual(self.safe_result['response_message'], 'SAFE Record added successfully. No transaction processed.')
        self.assertEqual(self.safe_result['response_code'], '1')
        self.assertEqual(self.safe_result['safe_id'], '1035593')

    @httpretty.activate
    def testFailedSAFEAdd(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/AGMS_SAFE_API.asmx",
                                body=self.failed_SAFEAdd_response(),
                                content_type="application/xml")

        params = {
            'payment_type': {'value': 'creditcard'},
            'first_name': {'value': 'Joe'},
            'last_name': {'value': 'Smith'},
            'cc_number': {'value': '4111111111111111'},
            'cc_exp_date': {'value': '0500'},
            'cc_cvv': {'value': '123'}
        }
        self.safe_result = self.safe.add(params)
        self.assertEqual(self.safe.response.is_successful(), True)
        self.assertEqual(self.safe_result['response_message'], 'SAFE Record added successfully. No transaction processed.')
        self.assertEqual(self.safe_result['response_code'], '1')
        self.assertEqual(self.safe_result['safe_id'], '1035595')

    @httpretty.activate
    def testSuccessfulSAFEUpdate(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/AGMS_SAFE_API.asmx",
                                body=self.successful_SAFEAdd_response(),
                                content_type="application/xml")
        params = {
            'payment_type': {'value': 'creditcard'},
            'first_name': {'value': 'Joe'},
            'last_name': {'value': 'Smith'},
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0500'},
            'cc_cvv': {'value': '123'}
        }
        self.safe_result = self.safe.add(params)
        self.assertEqual(self.safe.response.is_successful(), True)
        self.assertEqual(self.safe_result['response_message'], 'SAFE Record added successfully. No transaction processed.')
        self.assertEqual(self.safe_result['response_code'], '1')

        safe_id = self.safe.response.get_safe_id()

        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/AGMS_SAFE_API.asmx",
                                body=self.successful_SAFEUpdate_response(),
                                content_type="application/xml")
        params = {
            'payment_type': {'value': 'creditcard'},
            'first_name': {'value': 'Joe'},
            'last_name': {'value': 'Smith'},
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'},
            'safe_id': {'value': safe_id},
        }

        self.safe_result = self.safe.update(params)
        self.assertEqual(self.safe.response.is_successful(), True)
        self.assertEqual(self.safe_result['response_message'], 'SAFE Record updated successfully. No transaction processed.')
        self.assertEqual(self.safe_result['response_code'], '1')
        self.assertEqual(self.safe_result['safe_id'], '1035596')

    @httpretty.activate
    def testFailedSAFEUpdate(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/AGMS_SAFE_API.asmx",
                                body=self.successful_SAFEAdd_response(),
                                content_type="application/xml")
        params = {
            'payment_type': {'value': 'creditcard'},
            'first_name': {'value': 'Joe'},
            'last_name': {'value': 'Smith'},
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0500'},
            'cc_cvv': {'value': '123'}
        }
        self.safe_result = self.safe.add(params)
        self.assertEqual(self.safe.response.is_successful(), True)
        self.assertEqual(self.safe_result['response_message'], 'SAFE Record added successfully. No transaction processed.')
        self.assertEqual(self.safe_result['response_code'], '1')

        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/AGMS_SAFE_API.asmx",
                                body=self.failed_SAFEUpdate_response(),
                                content_type="application/xml")

        params = {
            'payment_type': {'value': 'creditcard'},
            'first_name': {'value': 'Joe'},
            'last_name': {'value': 'Smith'},
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'},
            'safe_id': {'value': '123'},
        }
        try:
            self.safe_result = self.safe.update(params)
        except ResponseException, e:
            self.assertEqual(str(e),'Transaction failed with error code 3 and message SAFE Record failed to update successfully.  No transaction processed. ')

    @httpretty.activate
    def testSuccessfulSAFEDelete(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/AGMS_SAFE_API.asmx",
                                body=self.successful_SAFEAdd_response(),
                                content_type="application/xml")

        params = {
            'payment_type': {'value': 'creditcard'},
            'first_name': {'value': 'Joe'},
            'last_name': {'value': 'Smith'},
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0500'},
            'cc_cvv': {'value': '123'}
        }
        self.safe_result = self.safe.add(params)
        self.assertEqual(self.safe.response.is_successful(), True)
        self.assertEqual(self.safe_result['response_message'], 'SAFE Record added successfully. No transaction processed.')
        self.assertEqual(self.safe_result['response_code'], '1')

        safe_id = self.safe.response.get_safe_id()
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/AGMS_SAFE_API.asmx",
                                body=self.successful_SAFEDelete_response(),
                                content_type="application/xml")

        params = {
            'safe_id': {'value': safe_id},
        }
        self.safe_result = self.safe.delete(params)
        self.assertEqual(self.safe.response.is_successful(), True)
        self.assertEqual(self.safe_result['response_message'], 'SAFE record has been deactivated')
        self.assertEqual(self.safe_result['response_code'], '1')

    @httpretty.activate
    def testFailedSAFEDelete(self):
        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/AGMS_SAFE_API.asmx",
                                body=self.successful_SAFEAdd_response(),
                                content_type="application/xml")

        params = {
            'payment_type': {'value': 'creditcard'},
            'first_name': {'value': 'Joe'},
            'last_name': {'value': 'Smith'},
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0500'},
            'cc_cvv': {'value': '123'}
        }
        self.safe_result = self.safe.add(params)
        self.assertEqual(self.safe.response.is_successful(), True)
        self.assertEqual(self.safe_result['response_message'], 'SAFE Record added successfully. No transaction processed.')
        self.assertEqual(self.safe_result['response_code'], '1')

        httpretty.register_uri(httpretty.POST, "https://gateway.agms.com/roxapi/AGMS_SAFE_API.asmx",
                                body=self.failed_SAFEDelete_response(),
                                content_type="application/xml")

        params = {
            'safe_id': {'value': '1234'},
        }
        self.safe_result = self.safe.delete(params)
        self.assertEqual(self.safe.response.is_successful(), True)
        self.assertEqual(self.safe_result['response_message'], 'SAFE record failed to deactivate')
        self.assertEqual(self.safe_result['response_code'], '2')

    def successful_SAFEAdd_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><AddToSAFEResponse xmlns=\"https://gateway.agms.com/roxapi/\"><AddToSAFEResult><STATUS_CODE>1</STATUS_CODE><STATUS_MSG>SAFE Record added successfully. No transaction processed.</STATUS_MSG><TRANS_ID /><AUTH_CODE /><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID>1035593</SAFE_ID><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID /><CUSTOMER_MESSAGE /><RRN /></AddToSAFEResult></AddToSAFEResponse></soap:Body></soap:Envelope>
            """

    def failed_SAFEAdd_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><AddToSAFEResponse xmlns=\"https://gateway.agms.com/roxapi/\"><AddToSAFEResult><STATUS_CODE>1</STATUS_CODE><STATUS_MSG>SAFE Record added successfully. No transaction processed.</STATUS_MSG><TRANS_ID /><AUTH_CODE /><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID>1035595</SAFE_ID><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID /><CUSTOMER_MESSAGE /><RRN /></AddToSAFEResult></AddToSAFEResponse></soap:Body></soap:Envelope>
            """

    def successful_SAFEUpdate_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><UpdateSAFEResponse xmlns=\"https://gateway.agms.com/roxapi/\"><UpdateSAFEResult><STATUS_CODE>1</STATUS_CODE><STATUS_MSG>SAFE Record updated successfully. No transaction processed.</STATUS_MSG><TRANS_ID /><AUTH_CODE /><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID>1035596</SAFE_ID><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID /><CUSTOMER_MESSAGE /><RRN /></UpdateSAFEResult></UpdateSAFEResponse></soap:Body></soap:Envelope>
            """

    def failed_SAFEUpdate_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><UpdateSAFEResponse xmlns=\"https://gateway.agms.com/roxapi/\"><UpdateSAFEResult><STATUS_CODE>3</STATUS_CODE><STATUS_MSG>SAFE Record failed to update successfully.  No transaction processed. </STATUS_MSG><TRANS_ID /><AUTH_CODE /><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID /><CUSTOMER_MESSAGE /><RRN /></UpdateSAFEResult></UpdateSAFEResponse></soap:Body></soap:Envelope>
            """

    def successful_SAFEDelete_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><DeleteFromSAFEResponse xmlns=\"https://gateway.agms.com/roxapi/\"><DeleteFromSAFEResult><STATUS_CODE>1</STATUS_CODE><STATUS_MSG>SAFE record has been deactivated</STATUS_MSG><TRANS_ID /><AUTH_CODE /><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID /><CUSTOMER_MESSAGE /><RRN /></DeleteFromSAFEResult></DeleteFromSAFEResponse></soap:Body></soap:Envelope>
            """

    def failed_SAFEDelete_response(self):
        return """
            <?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><DeleteFromSAFEResponse xmlns=\"https://gateway.agms.com/roxapi/\"><DeleteFromSAFEResult><STATUS_CODE>2</STATUS_CODE><STATUS_MSG>SAFE record failed to deactivate</STATUS_MSG><TRANS_ID /><AUTH_CODE /><AVS_CODE /><AVS_MSG /><CVV2_CODE /><CVV2_MSG /><ORDERID /><SAFE_ID /><FULLRESPONSE /><POSTSTRING /><BALANCE /><GIFTRESPONSE /><MERCHANT_ID /><CUSTOMER_MESSAGE /><RRN /></DeleteFromSAFEResult></DeleteFromSAFEResponse></soap:Body></soap:Envelope>
            """

if __name__ == '__main__':
    unittest.main()