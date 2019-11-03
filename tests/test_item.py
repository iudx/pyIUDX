import unittest
import sys
sys.path.insert(1, '../pyIUDX')
from pyIUDX.rs import item
from pyIUDX.cat import cat


class ItemsTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.catalogue = cat.Catalogue("https://pudx.catalogue.iudx.org.in/catalogue/v1")
        attributes = {"tags": ["aqm"]}
        filters = ["id"]
        itemList = self.catalogue.getManyResourceItems(attributes=attributes,
                                                       filters=filters)
        self.aqms = item.Items("https://pudx.catalogue.iudx.org.in/catalogue/v1",
                               items=itemList)
        print("Getting " + str(len(itemList)) + " items")

    def test_get_latest(self):
        print("Getting latest values")
        self.aqms.latest()
        print(self.aqms[0].CO2_MIN.value)

    def test_get_during(self):
        print("Getting during values")
        self.aqms.during("2019-10-28T00:00:00.000Z",
                         "2019-10-29T00:00:00.000Z")
        print(self.aqms[0].CO2_MIN.value)


if __name__ == '__main__':
    unittest.main()

