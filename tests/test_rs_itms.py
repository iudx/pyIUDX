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
        self.testVector = {}
        ''' TODO: Make this independent of paths '''
        with open("./tests/testVector_flood.json", "r") as f:
            self.testVector = json.load(f)

    def test_get_latest(self):
        latestArray = self.testVector["latest"]
        for item in latestArray:
            data = self.rs.getLatestData(item)
            self.assertTrue(data)
            print(data)

    def test_get_during(self):
        duringArray = self.testVector["during"]
        for item in duringArray:
            data = self.rs.getDataDuring(item["id"],
                                         item["startTime"], item["endTime"])
            print(json.dumps(data, indent=4))
            self.assertTrue(data)

if __name__ == '__main__':
    unittest.main()
