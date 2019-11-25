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
        with open("tests/testVector.json", "r") as f:
            self.testVector = json.load(f)

    def test_get_latest(self):
        latestArray = self.testVector["latest"]
        for item in latestArray:
            data = self.rs.getLatestData(item)
            print(data)
            self.assertTrue(data)

    def test_get_during(self):
        duringArray = self.testVector["during"]
        for item in duringArray:
            data = self.rs.getDataDuring(item["id"],
                                         item["startTime"], item["endTime"])
            print(json.dumps(data, indent=4))
            self.assertTrue(data)

    def test_get_like(self):
        like_array = self.testVector["likeLatest"]
        for item in like_array:
            data = self.rs.getLatestDataValuesLike(item["id"],
                                         item["attributeName"], item["attributeValue"])
            print(json.dumps(data, indent=4))
            self.assertTrue(data)

    def test_get_like_during(self):
        likeBetween_array = self.testVector["likeDuring"]
        for item in likeBetween_array:
            data = self.rs.getDataValuesLikeDuring(item["id"], item["attributeName"],
                                                    item["attributeValue"], item["startTime"],
                                                    item["endTime"])
            print(json.dumps(data, indent=4))

    def test_get_between(self):
        between_array = self.testVector["between"]
        for item in between_array:
            data = self.rs.getDataValuesBetween(item["id"], item["attributeName"],
                                                item["minVal"], item["maxVal"])
            print(json.dumps(data, indent=4))
            self.assertTrue(data)

    def test_get_latest_around(self):
        around_array = self.testVector["around"]
        for item in around_array:
            data = self.rs.getLatestDataAround(item["id"], item["point"], item["radius"])
            print(data)

if __name__ == '__main__':
    unittest.main()
