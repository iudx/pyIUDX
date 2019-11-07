import unittest
import sys
import matplotlib.pyplot as plt
sys.path.insert(1, '../pyIUDX')
from pyIUDX.rs import item
from pyIUDX.cat import cat


class ItemsTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.catalogue = cat.Catalogue("https://pudx.catalogue.iudx.org.in/catalogue/v1")
        geo = {"circle": {"lat": 18.539107, "lon": 73.903987, "radius": 3000}}
        attributes = {"tags": ["aqm"]}
        filters = ["id"]
        itemList = self.catalogue.getManyResourceItems(attributes=attributes,
                                                       geo=geo,
                                                       filters=filters)
        self.aqms = item.Items("https://pudx.catalogue.iudx.org.in/catalogue/v1",
                               items=itemList)
        print("Getting " + str(len(itemList)) + " items")
        print(self.aqms[0].geoProperties)

    def test_get_latest(self):
        print("All quantitativeProperties")
        print(self.aqms[0].quantitativeProperties)
        print("Getting latest values")
        self.aqms.latest()
        print(self.aqms[0].CO2_MIN.value)

    def test_get_during(self):
        print("Getting during values")
        self.aqms.during("2019-11-06T17:00:00.000+05:30",
                         "2019-11-06T18:30:00.000+05:30")
        print(self.aqms[1].CO2_MIN.value)


if __name__ == '__main__':
    unittest.main()

