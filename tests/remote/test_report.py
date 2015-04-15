from __future__ import absolute_import
import unittest
from agms.configuration import Configuration
from agms.report import Report


class ReportTest(unittest.TestCase):

    def setUp(self):
        Configuration.configure('agmsdevdemo', 'nX1m*xa9Id', '1001789', 'b00f57326f8cf34bbb705a74b5fcbaa2b2f3e58076dc81f', 'requests')
        self.report = Report()
        
    def testReportClassAssignment(self):
        self.assertIsInstance(self.report, Report)

    def testSuccessfulTransactionAPI(self):
        params = {
            'start_date': {'value': '2015-03-25'},
            'end_date': {'value': '2015-03-31'},
        }
        report_result = self.report.list_transactions(params)
        print report_result
        self.assertIsInstance(report_result, list)

    def testSuccessfulSAFEAPI(self):
        params = {
            'start_date': {'value': '2015-03-25'},
            'end_date': {'value': '2015-03-31'},
        }
        report_result = self.report.list_SAFEs(params)
        self.assertIsInstance(report_result, list)


if __name__ == '__main__':
    unittest.main()