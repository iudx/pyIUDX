""" A python script example for using the ResourceServer class of pyIUDX SDK(https://github.com/iudx/pyIUDX)

This script allows the user to access the class-Items(class for a list of iudx resource items) from python SDK for IUDX(pyIUDX), 

This class can also be imported as a module and contains the following functions:
    *latest() - Get latest data, returns: updated object data
    *during(startTime, endTime) - Get data during a time interval, returns: numpy 2d array with 0th column as time
"""

"""Import item object from pyIUDX SDK
"""
from pyIUDX.rs import item


"""List of IDs of the resource items, this can be obtained by querying the catalogue for IDs of resource items for a particular tag or a particular geographical boundary or a particular resource group
"""
itemList = [{"id": "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/aqm-bosch-climo/Karve Statue Square_5"},
{"id": "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/aqm-bosch-climo/Bajaj Statue Square_50"},
{"id": "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/aqm-bosch-climo/BRTS Visharant wadi_38"},
{"id": "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/aqm-bosch-climo/Datta Mandir Square_20"},
{"id": "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/aqm-bosch-climo/Seven Loves Square_16"}]

"""Creating a new object element of type Items from rs of pyIUDX
"""
element = item.Items("https://pudx.catalogue.iudx.org.in/catalogue/v1", items=itemList)

"""A python snippet to get quantitative Properties of the resource item or of the resource group(if the items in the list belong to the same resource group)
"""
print(element[0].quantitativeProperties)

""" A python snippet to get latest value of the quantitativeProperties for the resource item/ resource items
"""
element.latest()
for i in range(len(itemList)):
    print(element[i].CO_MAX.value)

"""A python snippet to get value of the quantitativeProperties during a set time interval for the resource item/ resource items
"""
air = element[0].during("2019-11-05T10:00:00.000+05:30","2019-11-05T12:00:00.000+05:30")
print(air.CO_MAX.value)
