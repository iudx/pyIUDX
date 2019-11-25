import unittest
import sys
sys.path.insert(1, '../pyIUDX')
from pyIUDX.rs import item
from pyIUDX.cat import cat

def printer(item):
    print("Time\t Bus number\t Location")
    print("{0: <30}".format("Time") +
          "{0: <30}".format("Bus Number") +
          "{0: <30}".format("Latitude") +
          "{0: <30}".format("Longitude"))
    print("\n")
    for values in zip(item.ROUTE_ID.value,
                      item.LATITUDE_STR.coordinates,
                      item.LONGITUDE_STR.coordinates):
        print("{0: <30}".format(str(values[0][0])) +
              "{0: <30}".format(str(values[0][1])) +
              "{0: <30}".format(str(values[1][1])) +
              "{0: <30}".format(str(values[2][1])))

class ItemsTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.catalogue = cat.Catalogue("https://pudx.catalogue.iudx.org.in/catalogue/v1")
        self.itms = item.Item("https://pudx.catalogue.iudx.org.in/catalogue/v1",
                              "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/pune-itms/pune-itms-live")
        print(self.itms.timeProperties)

    def test_get_latest(self):
        print(self.itms.geoProperties)
        self.itms.latest()
        print(self.itms.LONGITUDE_STR.coordinates)

    def test_get_during(self):
        print("Getting during values")
        self.itms.during("2019-11-07T16:00:00.000+05:30",
                         "2019-11-07T16:30:00.000+05:30")
        printer(self.itms)

    def test_get_latest_with(self):
        print("Getting Latest for a bus")
        self.itms.latestWith("ROUTE_ID", "148")
        printer(self.itms)
        


if __name__ == '__main__':
    unittest.main()

