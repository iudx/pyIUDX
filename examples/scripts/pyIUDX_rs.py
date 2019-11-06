""" A python script example for using the ResourceServer class of pyIUDX SDK(https://github.com/iudx/pyIUDX)

This script allows the user to access the class-ResourceServer from python SDK for IUDX(pyIUDX)
This class can also be imported as a module and contains the following functions:
    *dispParams() - Display rs initalization parameter, returns: version string
    *getData(id, opts=None, token=None) - Get data from a resource server, returns: rs constructed url
    *getDataAfter(id, time, token=None) - Get data after a given time, returns: corresponding data as a list of dicts/dict
    *getDataAround(id, point, radius, token=None) - Get data around a specific point(lat, lon) and radius(meters), returns: corresponding data as a list of dicts/dict
    *getDataBefore(id, time, token=None) - Get data before a given time, returns: corresponding data as a list of dicts/dict
    *getDataDuring(id, startTime, endTime, token=None) - Get data during a time interval, returns: corresponding data as a list of dicts/dict
    *getDataValuesBetween(id, attribute, minVal, maxVal, token=None) - Get data of an item for which an attribute is between minVal and maxVal, returns: corresponding data as a list of dicts/dict
    *getDataValuesGreater(id, attribute, minVal, token=None) - Get data of an item for which an attribute is greater than minVal, returns: corresponding data as a list of dicts/dict
    *getDataValuesLesser(id, attribute, maxVal, token=None) - Get data of an item for which an attribute is lesser than maxVal, returns: corresponding data as a list of dicts/dict
    *getDataValuesLike(id, attribute, val, token=None) - Get data of an item for which an attribute is like value, returns: corresponding data as a list of dicts/dict
    *getLatestData(id, token=None) - Get latest data, returns: corresponding data as a list of dicts/dict
    *getStatus(id, token=None) - Get Status of a resource item, returns: corresponding data as a list of dicts/dict
    *getUrl() - Get rs constructed url, returns: rs constructed url
    *search(url, data) - Use requests library to make a search request, returns: Response body
"""

"""Import rs object from pyIUDX SDK
"""
from pyIUDX.rs import rs

"""Creating a new object resource of type ResourceServer from rs of pyIUDX
"""
resource = rs.ResourceServer("https://pudx.resourceserver.iudx.org.in/resource-server/pscdcl/v1")


"""A python snippet to get the status for the particular resource ID from the PUDX resource server
"""

"""ID of the resource item
"""
id = "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/aqm-bosch-climo/Karve Statue Square_5"

status = resource.getStatus(id)
print("Status of resource item "+ id.split("/")[3] + " at " + id.split("/")[4] + " is:-", end=" ")
print(status)

"""A python snippet to get latest data available for a particular resource identified by its ID from PUDX resource server
"""

"""ID of the resource item
"""
id = "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/aqm-bosch-climo/Karve Statue Square_5"

latestData = resource.getLatestData(id)
print("Latest available data for resource item "+ id.split("/")[3] + " at " + id.split("/")[4] + " is:- ")
print(latestData)

"""A python snippet to get data for a particular resource identified by its ID for a time duration from PUDX resource server
"""

"""ID of the resource item
"""
id = "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/aqm-bosch-climo/Karve Statue Square_5"

startTime = "2019-10-30T00:00:00.000Z"
endTime = "2019-11-01T00:00:00.000Z"

data = resource.getDataDuring(id, startTime, endTime)
print("Data from resource item "+ id.split("/")[3] + " at " + id.split("/")[4] + " for the duration between " + startTime + " to " + endTime + " is:- ")
print(data)

"""A python snippet to get data for a particular resource identified by its ID for the entire time either before or after the specified time from PUDX resource server
"""

"""ID of the resource item
"""
id = "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/aqm-bosch-climo/Karve Statue Square_5"

time = "2019-10-30T00:00:00.000Z"

data = resource.getDataAfter(id, time)
print("Data from resource item "+ id.split("/")[3] + " at " + id.split("/")[4] + " after " + time + " is:- ")
print(data)

data = resource.getDataBefore(id, time)
print("Data from resource item "+ id.split("/")[3] + " at " + id.split("/")[4] + " before " + time + " is:- ")
print(data)
