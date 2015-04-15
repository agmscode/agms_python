from __future__ import absolute_import
import unittest
from agms.version import Version


class VersionTest(unittest.TestCase):
    def testVersion(self):
        self.assertEqual(Version, "0.1.0")


if __name__ == '__main__':
    unittest.main()