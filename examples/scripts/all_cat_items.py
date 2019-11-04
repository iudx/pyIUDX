"""Get all catalogue entries from PUDX

An example python script to fetch all items in the PUDX catalogue
The script gives all the catalogue item entries and the total count of items
"""

"""Import cat object from pyIUDX SDK
"""
from pyIUDX.cat import cat

"""Creating a new object records of type Catalogue from cat of pyIUDX
"""
records = cat.Catalogue("https://pudx.catalogue.iudx.org.in/catalogue/v1")

"""Fetch all items in the PUDX Catalogue
"""
allCatItems = records.getAllItems()
print(allCatItems)

"""Get count all items of PUDX Catalogue
"""
allCatItemCount = records.getItemCount()
print(allCatItemCount)
