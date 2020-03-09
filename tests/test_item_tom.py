import unittest
import sys
sys.path.insert(1, '../pyIUDX')
from pyIUDX.rs import item
from pyIUDX.cat import cat


class ItemsTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.catalogue = cat.Catalogue("https://pudx.catalogue.iudx.org.in/catalogue/v1")
        self.incidents = item.Item("https://pudx.catalogue.iudx.org.in/catalogue/v1",
                                   "https://pudx.resourceserver.iudx.org.in/resource-server/pscdcl/v1",
                                   "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/tomtom/pune-traffic-incidents")
        print("====== Static =========")
        print(self.incidents.properties)
        print(self.incidents.geoProperties)
        print(self.incidents.timeProperties)
        print(self.incidents.quantitativeProperties)

    def test_get_during(self):
        print("Getting during values")

        self.incidents.during("2019-11-09T00:00:00.000+05:30",
                              "2019-11-11T14:30:00.000+05:30")
        print("Incidents during ")
        print("{0: <30}".format("Time") +
              "{0: <30}".format("Road Name") +
              "{0: <30}".format("Incident") +
              "{0: <30}".format("Incident Description") +
              "{0: <30}".format("Location"))
        print("\n")
        for values in zip(self.incidents.incident.value,
                          self.incidents.incidentRoadName.value,
                          self.incidents.incidentDescription.value,
                          self.incidents.incidentLocation.coordinates):
            print("{0: <30}".format(str(values[0][0])) +
                  "{0: <30}".format(str(values[1][1])) +
                  "{0: <30}".format(str(values[0][1])) +
                  "{0: <30}".format(str(values[2][1])) +
                  "{0: <30}".format(str(values[3][1])))


if __name__ == '__main__':
    unittest.main()

