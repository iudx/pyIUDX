""" Get IDs of catalogue entries filtered by attributes for geographical boundary from PUDX

An example python script to fetch catalogue entries for a particular group of resource from the PUDX catalogue
"""

"""Import cat object from pyIUDX SDK
"""
from pyIUDX.cat import cat

"""Creating a new object records of type Catalogue from cat of pyIUDX
"""
records = cat.Catalogue("https://pudx.catalogue.iudx.org.in/catalogue/v1")

"""Setting attributes to filter by tags(aqm in this example)
"""
attributes = {"tags": ["aqi", "aqm"]}

"""Filtering fields from the PUDX item (id in this case)
"""
filters = ["id"]

"""Filtering a catalogue by a geographical bound, which could be a -    polygon,
                                                                        cirlce,
                                                                        line,
                                                                        bbox (polygon in this example).
"""
geo = {"polygon": [[18.4, 73.9], [21.6, 78.9], [27.1, 80], [30, 75.25],[25.7, 74.7], [18.4, 73.9]]}

"""Fetch IDs of resource items from the catalogue for the set attribute filter(aqm in this case) within the geographical boundary from the PUDX Catalogue
"""
items = cat.getManyResourceItems(attributes=attributes,filters=filters, geo=geo)
print(items)

"""Get count all IDs fetched from the PUDX Catalogue
"""
count = cat.getItemCount(attributes=attributes,filters=filters, geo=geo)
print(count)
