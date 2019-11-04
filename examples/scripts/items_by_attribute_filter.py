""" Get items for a particular resource group filtered by attributes from PUDX

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

"""Fetch all catalogue items for the set attribute filter(aqm in this case) from the PUDX Catalogue
"""
allAQMItems = records.getManyResourceItems(attributes)
print(allAQMItems)

"""Get count all items of PUDX Catalogue
"""
allAQMItemsCount = records.getItemCount(attributes)
print(allAQMItemsCount)
