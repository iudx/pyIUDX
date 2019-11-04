""" Get IDs of catalogue entries filtered by attributes from PUDX

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

"""Fetch IDs of resource items from the catalogue for the set attribute filter(aqm in this case) from the PUDX Catalogue
"""
allAQMItemsID = records.getManyResourceItems(attributes, filters)
print(allAQMItemsID)

"""Get count all IDs fetched from the PUDX Catalogue
"""
allAQMItemsCount = records.getItemCount(attributes, filters)
print(allAQMItemsCount)
