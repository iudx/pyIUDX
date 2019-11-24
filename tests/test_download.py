'''
    This script creates a test user and display
'''
import unittest
import sys
import json
sys.path.insert(1, '../pyIUDX')
from pyIUDX.rs import rs


class RSTest(unittest.TestCase):
    ''' Test different scenarios '''

    def __init__(self, *args, **kwargs):
        super(RSTest, self).__init__(*args, **kwargs)
        self.rs = rs.ResourceServer("https://pudx.resourceserver.iudx.org.in/resource-server/pscdcl/v1")

    def test_get_during(self):
        data = self.rs.downloadData("urn:iudx-catalogue-pune:pudx-resource-server/pune-itms")
        print(data)
        self.assertTrue(data)

if __name__ == '__main__':
    unittest.main()
