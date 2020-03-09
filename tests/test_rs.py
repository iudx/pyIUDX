'''
    This script creates a test user and display
'''
import unittest
import sys
import json
sys.path.insert(1, '../pyIUDX')
from pyIUDX.item import Item


class RSTest(unittest.TestCase):
    ''' Test different scenarios '''

    def __init__(self, *args, **kwargs):
        super(RSTest, self).__init__(*args, **kwargs)
        self.testVector = {}
        ''' TODO: Make this independent of paths '''
        with open("tests/testVector.json", "r") as f:
            self.testVector = json.load(f)

    def test_get_latest(self):
        latestArray = self.testVector["latest"]
        for item in latestArray:
            data = Item(item).latest().get()
            print(data)
            self.assertTrue(data)

    def test_get_during(self):
        duringArray = self.testVector["during"]
        for item in duringArray:
            data = Item(item["id"]).during(item["startTime"],
                                                  item["endTime"]).get()
            print(json.dumps(data, indent=4))
            self.assertTrue(data)

    def test_get_like_latest(self):
        like_array = self.testVector["likeLatest"]
        for item in like_array:
            data = Item(item["id"]).latest().like(item["attributeName"],\
                                                         item["attributeValue"])\
                                          .get()
            print(json.dumps(data, indent=4))
            self.assertTrue(data)

    def test_get_like_during(self):
        likeBetween_array = self.testVector["likeDuring"]
        for item in likeBetween_array:
            data = Item(item["id"]).during(item["startTime"], item["endTime"])\
                                          .like(item["attributeName"],item["attributeValue"])\
                                          .get()
            print(json.dumps(data, indent=4))


if __name__ == '__main__':
    unittest.main()
