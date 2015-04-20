from __future__ import absolute_import
import unittest
from agms.configuration import Configuration
from agms.invoicing import Invoicing


class InvoicingTest(unittest.TestCase):

    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', None, None, 'requests')
        self.invoicing = Invoicing()
        
    def testInvoicingClassAssignment(self):
        self.assertTrue(isinstance(self.invoicing, Invoicing))


if __name__ == '__main__':
    unittest.main()