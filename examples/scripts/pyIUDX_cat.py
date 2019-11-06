""" A python script example for using the Catalogue class of pyIUDX SDK(https://github.com/iudx/pyIUDX)

This script allows the user to access the class-Catalogue from python SDK for IUDX(pyIUDX)
This class can also be imported as a module and contains the following functions:
    *checkConnection() - Establishes connection to the catalogue URL, returns: None
    *getAllItems() - Get all catalogue items, returns: List of catalogue items
    *getDataModel(id) - Get the data model for a given id, returns: List of catalogue items
    *getItemCount(attributes=None, filters=None, geo=None) - Number of items matching the criterion, returns: number of items or -1 if fail
    *getManyResourceItems(attributes=None, filters=None, geo=None) - Items matching the criterion, returns: List of catalogue items
    *getOneResourceItem(id, filters=None) - Item given the id, returns: A catalogue item
    *makeOpts(attributes=None, filters=None, geo=None) - returns: options as a string for a GET method
"""

"""Import cat object from pyIUDX SDK
"""
from pyIUDX.cat import cat

"""Creating a new object records of type Catalogue from cat of pyIUDX
"""
records = cat.Catalogue("https://pudx.catalogue.iudx.org.in/catalogue/v1")


"""A python snippet to fetch all items in the PUDX catalogue
The script gives all the catalogue item entries and the total count of items
"""
allCatItems = records.getAllItems()
print(allCatItems)

allCatItemCount = records.getItemCount()
print(allCatItemCount)


"""A python snippet to fetch catalogue entry for a particular resource ID in the PUDX catalogue
"""

"""ID of the resource item
"""
id = ('rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/aqm-bosch-climo/Datta Mandir Square_20')

AQMItem = records.getOneResourceItem(id)
print(AQMItem)


"""A python snippet to fetch catalogue entries for a particular group of resource(aqm in this case) from the PUDX catalogue and
the count of items for the particular resource group
"""

"""Setting attributes to filter by tags(aqm in this example)
"""
attributes = {"tags": ["aqi", "aqm"]}

allAQMItems = records.getManyResourceItems(attributes)
print(allAQMItems)

allAQMItemsCount = records.getItemCount(attributes)
print(allAQMItemsCount)



"""A python snippet to fetch the IDs for a particular group of resource from the PUDX catalogue and the count of 
IDs for the particular resource group
"""

"""Setting attributes to filter by tags(aqm in this example)
"""
attributes = {"tags": ["aqi", "aqm"]}

"""Filtering fields from the PUDX item (id in this case)
"""
filters = ["id"]

allAQMItemsID = records.getManyResourceItems(attributes, filters)
print(allAQMItemsID)

allAQMItemsCount = records.getItemCount(attributes, filters)
print(allAQMItemsCount)


"""A python snippet to fetch catalogue entries for a particular group of resource from the PUDX catalogue which lie within 
the specified geographical boundary the count of items for the particular resource group within the geographical boundary
"""

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

items = records.getManyResourceItems(attributes=attributes,filters=filters, geo=geo)
print(items)

count = records.getItemCount(attributes=attributes,filters=filters, geo=geo)
print(count)
