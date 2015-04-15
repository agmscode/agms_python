from __future__ import absolute_import
import unittest
from agms.configuration import Configuration
from agms.safe import SAFE
from agms.exception.response_exception import ResponseException


class SAFETest(unittest.TestCase):

    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', None, None, 'requests')
        self.safe = SAFE()
        
    def testSAFEClassAssignment(self):
        self.assertIsInstance(self.safe, SAFE)

    def testSuccessfulSAFEAdd(self):
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
        self.assertEqual(self.safe_result['response_message'],
                         'SAFE Record added successfully. No transaction processed.')
        self.assertEqual(self.safe_result['response_code'], '1')

    def testFailedSAFEAdd(self):
        params = {
            'payment_type': {'value': 'creditcard'},
            'first_name': {'value': 'Joe'},
            'last_name': {'value': 'Smith'},
            'cc_number': { 'value': '4111111111111111'},
            'cc_exp_date': {'value': '0500'},
            'cc_cvv': {'value': '123'}
        }
        # Todo fail the transaction
        self.safe_result = self.safe.add(params)
        self.assertEqual(self.safe.response.is_successful(), True)
        self.assertEqual(self.safe_result['response_message'],
                         'SAFE Record added successfully. No transaction processed.')
        self.assertEqual(self.safe_result['response_code'], '1')

    def testSuccessfulSAFEUpdate(self):
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
        self.assertEqual(self.safe_result['response_message'],
                         'SAFE Record added successfully. No transaction processed.')
        self.assertEqual(self.safe_result['response_code'], '1')

        safe_id = self.safe.response.get_safe_id()
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
        self.assertEqual(self.safe_result['response_message'],
                         'SAFE Record updated successfully. No transaction processed.')
        self.assertEqual(self.safe_result['response_code'], '1')

    def testFailedSAFEUpdate(self):
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
            self.assertEqual(str(e),
                             'Transaction failed with error code 3 and message SAFE Record failed to update successfully.  No transaction processed. ')

    def testSuccessfulSAFEDelete(self):
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
        self.assertEqual(self.safe_result['response_message'],
                         'SAFE Record added successfully. No transaction processed.')
        self.assertEqual(self.safe_result['response_code'], '1')

        safe_id = self.safe.response.get_safe_id()

        params = {
            'safe_id': {'value': safe_id},
        }
        self.safe_result = self.safe.delete(params)
        self.assertEqual(self.safe.response.is_successful(), True)
        self.assertEqual(self.safe_result['response_message'], 'SAFE record has been deactivated')
        self.assertEqual(self.safe_result['response_code'], '1')

    def testFailedSAFEDelete(self):
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
        self.assertEqual(self.safe_result['response_message'],
                         'SAFE Record added successfully. No transaction processed.')
        self.assertEqual(self.safe_result['response_code'], '1')

        params = {
            'safe_id': {'value': '1234'},
        }
        self.safe_result = self.safe.delete(params)
        self.assertEqual(self.safe.response.is_successful(), True)
        self.assertEqual(self.safe_result['response_message'], 'SAFE record failed to deactivate')
        self.assertEqual(self.safe_result['response_code'], '2')


if __name__ == '__main__':
    unittest.main()