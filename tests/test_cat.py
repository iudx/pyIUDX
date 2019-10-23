'''
    This script creates a test user and display
'''
import unittest
import sys
sys.path.insert(1, '../pyIUDX')
from pyIUDX.cat import cat


class CatTest(unittest.TestCase):
    ''' Test different scenarios '''

    def __init__(self, *args, **kwargs):
        super(CatTest, self).__init__(*args, **kwargs)
        self.catalogue = cat.Catalogue("https://catalogue.iudx.org.in", "443")

    def test_get_count(self):
        attributes = {"tags": ["aqi", "aqm"]}
        count = self.catalogue.getItemCount(attributes=attributes)
        self.assertNotEqual(count, -1)
        self.assertNotEqual(count, 0)

    def test_get_one(self):
        id = ('rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pscdcl/'
              'aqm-bosch-climo/Datta Mandir Square_20')
        item = self.catalogue.getOneResourceItem(id)
        self.assertTrue(item)

    def test_get_many_one_attr_one_filter(self):
        attributes = {"tags": ["aqi", "aqm"]}
        filters = ["id"]
        items = self.catalogue.getManyResourceItems(attributes=attributes,
                                                    filters=filters)
        self.assertTrue(items)

    def test_get_many_geo(self):
        geo = {"polygon": [[18.4, 73.9], [21.6, 78.9], [27.1, 80], [30, 75.25],
                           [25.7, 74.7], [18.4, 73.9]]}
        items = self.catalogue.getManyResourceItems(geo=geo)
        self.assertTrue(items)

    def test_get_many_geo_attribute_filter(self):
        geo = {"polygon": [[18.4, 73.9], [21.6, 78.9], [27.1, 80], [30, 75.25],
                           [25.7, 74.7], [18.4, 73.9]]}
        filters = ["id"]
        attributes = {"tags": ["aqi", "aqm"]}
        items = self.catalogue.getManyResourceItems(attributes=attributes,
                                                    filters=filters, geo=geo)
        self.assertTrue(items)


if __name__ == '__main__':
    unittest.main()
