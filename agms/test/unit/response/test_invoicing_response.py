from __future__ import absolute_import
import unittest
from agms.invoicing import Invoicing


class InvoicingResponseTest(unittest.TestCase):
    def setUp(self):
        self.invoicing = Invoicing()

    def testInvoicingClassAssignment(self):
        self.assertEqual('Not Implemented', 'Not Implemented')


if __name__ == '__main__':
    unittest.main()