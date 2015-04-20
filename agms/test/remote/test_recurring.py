from __future__ import absolute_import
import unittest
from agms.configuration import Configuration
from agms.recurring import Recurring


class RecurringTest(unittest.TestCase):

    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', None, None, 'requests')
        self.recurring = Recurring()
        
    def testRecurringClassAssignment(self):
        self.assertTrue(isinstance(self.recurring, Recurring))

    
if __name__ == '__main__':
    unittest.main()