import unittest
import sys
sys.path.insert(1, '../pyIUDX')
from pyIUDX.rs import item
from pyIUDX.cat import cat


class ItemsTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.catalogue = cat.Catalogue("https://pudx.catalogue.iudx.org.in/catalogue/v1")
        self.itms = item.Item("https://pudx.catalogue.iudx.org.in/catalogue/v1",
                               "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/pune-itms/pune-itms-live")
        print(self.itms.properties)

    def test_get_latest(self):
        print(self.itms.geoProperties)
        self.itms.latest()
        print(self.itms.LONGITUDE_STR.coordinates)

    def test_get_during(self):
        print("Getting during values")
        self.itms.during("2019-11-04T10:00:00.000Z",
                         "2019-11-04T10:15:00.000Z")
        i = 0
        print("Time\t Bus number\t Location")
        for bus in self.itms.NAME.state:
            print(str(bus[0]) + "\t" + str(bus[1]) + "\t" + "[" +
                  str(self.itms.LATITUDE_STR.coordinates[i, 1]) + ", " +
                  str(self.itms.LONGITUDE_STR.coordinates[i, 1]) + "]")



if __name__ == '__main__':
    unittest.main()

