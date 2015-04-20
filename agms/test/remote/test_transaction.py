from __future__ import absolute_import
import unittest
from agms.configuration import Configuration
from agms.transaction import Transaction


class RemoteTransactionTest(unittest.TestCase):

    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', None, None, 'requests')
        self.transaction = Transaction()
        
    def testTransactionClassAssignment(self):
        self.assertTrue(isinstance(self.transaction, Transaction))

    def testTransactionOp(self):
        self.assertEqual(self.transaction._op, 'ProcessTransaction')
    
    def testTransactionProcess(self):
        params = {
            'transaction_type': {'value': 'sale'},
            'amount': {'value': '100.00'}, 
            'cc_number': {'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)

        self.assertTrue(isinstance(self.transaction, Transaction))
        self.assertEqual(self.transaction.request._fields['TransactionType']['value'], 'sale')
        self.assertTrue(isinstance(self.transaction.response.to_array(), dict))

    def testSuccessfulSale(self):
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

    def testFailedSale(self):
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
    
    def testSuccessfulAuthorize(self):
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

    def testFailedAuthorize(self):
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
        self.assertEqual('Not Implemented', 'Not Implemented')

    def testSuccessfulCapture(self):
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

        auth_code = self.transaction.response.get_authorization()

        params = {
            'transaction_type': {'value': 'capture'},
            'transaction_id': {'value': auth_code},
            'amount': {'value': '10'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Capture successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')
        
    def testPartialCapture(self):
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

        auth_code = self.transaction.response.get_authorization()

        params = {
            'transaction_type': {'value': 'capture'},
            'transaction_id': {'value': auth_code},
            'amount': {'value': '5'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Capture successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

    def testFailedCapture(self):
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

        auth_code = self.transaction.response.get_authorization()

        params = {
            'transaction_type': {'value': 'capture'},
            'transaction_id': {'value': auth_code},
            'amount': {'value': '0.01'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Capture successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

    def testSuccessfulRefund(self):
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

        auth_code = self.transaction.response.get_authorization()

        params = {
            'transaction_type': {'value': 'refund'},
            'transaction_id': {'value': auth_code},
            'amount': {'value': '10'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'refund successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

    def testPartialRefund(self):
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

        auth_code = self.transaction.response.get_authorization()

        params = {
            'transaction_type': {'value': 'refund'},
            'transaction_id': {'value': auth_code},
            'amount': {'value': '5'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'refund successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

    def testFailedRefund(self):
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

        auth_code = self.transaction.response.get_authorization()

        params = {
            'transaction_type': {'value': 'refund'},
            'transaction_id': {'value': auth_code},
            'amount': {'value': '20'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Transaction with type refund must include an amount that is equal or less then the original amount.  ')
        self.assertEqual(self.transaction_result['response_code'], '2')

    def testSuccessfulVoid(self):
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

        auth_code = self.transaction.response.get_authorization()

        params = {
            'transaction_type': {'value': 'void'},
            'transaction_id': {'value': auth_code}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'void successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

    def testFailedVoid(self):
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

        auth_code = self.transaction.response.get_authorization()

        params = {
            'transaction_type': {'value': 'void'},
            'transaction_id': {'value': auth_code}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'void successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

    def testSuccessfulVerify(self):
        params = {
            'transaction_type': {'value': 'auth'},
            'amount': {'value': '1.00'}, 
            'cc_number': {'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

        auth_code = self.transaction.response.get_authorization()

        params = {
            'transaction_type': {'value': 'void'},
            'transaction_id': {'value': auth_code}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'void successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

    def testFailedVerify(self):
        params = {
            'transaction_type': {'value': 'auth'},
            'amount': {'value': '1.00'}, 
            'cc_number': {'value': '4111111111111111'},
            'cc_exp_date': {'value': '0520'},
            'cc_cvv': {'value': '123'}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')

        auth_code = self.transaction.response.get_authorization()
        params = {
            'transaction_type': {'value': 'void'},
            'transaction_id': {'value': auth_code}
        }
        self.transaction_result = self.transaction.process(params)
        self.assertEqual(self.transaction.response.is_successful(), True)
        self.assertEqual(self.transaction_result['response_message'], 'void successful: Approved')
        self.assertEqual(self.transaction_result['response_code'], '1')


if __name__ == '__main__':
    unittest.main()