""" Get data for a particular resource identified by its ID for a time duration from PUDX resource server

An example python script to give data only for the time frame specified of a particular resource from the PUDX resource server 
"""

"""Import rs object from pyIUDX SDK
"""
from pyIUDX.rs import rs

"""Creating a new object records of type ResourceServer from rs of pyIUDX
"""
resource = rs.ResourceServer("https://pudx.resourceserver.iudx.org.in/resource-server/pscdcl/v1")

"""ID of the resource item
"""
id = "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pudx-resource-server/aqm-bosch-climo/Karve Statue Square_5"

"""Start time from which the data for the particular resource is required
"""
startTime = "2019-10-30T00:00:00.000Z"

"""Time till which the data for the particular resource is required
"""
endTime = "2019-11-01T00:00:00.000Z"

"""Get data for the particular resource ID for the time frame specified from the PUDX resource server
"""
data = resource.getDataDuring(id, startTime, endTime)
print(data)
