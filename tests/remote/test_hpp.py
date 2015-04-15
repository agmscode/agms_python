from __future__ import absolute_import
import unittest
from agms.configuration import Configuration
from agms.hpp import HPP


class HPPTest(unittest.TestCase):

    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', '1001789', 'b00f57326f8cf34bbb705a74b5fcbaa2b2f3e58076dc81f', 'requests')
        self.hpp = HPP()
        
    def testHPPClassAssignment(self):
        self.assertIsInstance(self.hpp, HPP)

    def testSuccessfulHPPGetHash(self):
        params = {
            'transaction_type': {'value': 'sale'},
            'amount': {'value': '20.00'}, 
            'first_name': {'setting': 'required'},
            'last_name': {'setting': 'required'},
            'zip': {'setting': 'required'},
            'email': {'setting': 'required'},
            'hpp_format': {'value': '1'},
        }
        self.hpp_result = self.hpp.generate(params)
        self.assertIsInstance(self.hpp.get_hash(), unicode)

    def testSuccessfulHPPGetLink(self):
        params = {
            'transaction_type': {'value': 'sale'},
            'amount': {'value': '20.00'}, 
            'first_name': {'setting': 'required'},
            'last_name': {'setting': 'required'},
            'zip': {'setting': 'required'},
            'email': {'setting': 'required'},
            'hpp_format': {'value': '1'},
        }
        self.hpp_result = self.hpp.generate(params)
        self.assertIsInstance(self.hpp.get_link(), unicode)


if __name__ == '__main__':
    unittest.main()