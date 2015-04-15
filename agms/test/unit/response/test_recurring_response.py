from __future__ import absolute_import
import unittest
from agms.recurring import Recurring


class RecurringResponseTest(unittest.TestCase):
    def setUp(self):
        self.recurring = Recurring()

    def testRecurringClassAssignment(self):
        self.assertEqual('Not Implemented', 'Not Implemented')


if __name__ == '__main__':
    unittest.main()