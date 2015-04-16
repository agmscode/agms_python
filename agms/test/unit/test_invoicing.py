from __future__ import absolute_import
import unittest
from agms.configuration import Configuration
from agms.invoicing import Invoicing


class InvoicingTest(unittest.TestCase):

    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', '1001789', 'b00f57326f8cf34bbb705a74b5fcbaa2b2f3e58076dc81f', 'requests')
        self.invoicing = Invoicing()
        
    def testInvoicingClassAssignment(self):
        self.assertTrue(isinstance(self.invoicing, Invoicing))

    
if __name__ == '__main__':
    unittest.main()