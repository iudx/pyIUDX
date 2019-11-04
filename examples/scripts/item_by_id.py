""" Get item of a particular resource by its ID from PUDX

An example python script to fetch catalogue entry for a particular resource ID in the PUDX catalogue
"""

"""Import cat object from pyIUDX SDK
"""
from pyIUDX.cat import cat

"""Creating a new object records of type Catalogue from cat of pyIUDX
"""
records = cat.Catalogue("https://pudx.catalogue.iudx.org.in/catalogue/v1")

"""ID of the resource item
"""
id = ('rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/aqm-bosch-climo/Datta Mandir Square_20')

"""Fetch catalogue item for the particular resource ID from the PUDX Catalogue
"""
AQMItem = records.getOneResourceItem(id)
print(AQMItem)
