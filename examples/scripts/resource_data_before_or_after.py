""" Get data for a particular resource identified by its ID for the entire time either before or after the specified time from PUDX resource server

An example python script to give data for the entire time either before or after the specified time for a particular resource from the PUDX resource server 
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

"""Time before/after which the data for the particular resource is required
"""
time = "2019-10-30T00:00:00.000Z"

"""Get all available data for the particular resource ID after the specified time from the PUDX resource server
"""
data = resource.getDataAfter(id, time)
print(data)

"""Get all available data for the particular resource ID before the specified time from the PUDX resource server
"""
data = resource.getDataBefore(id, time)
print(data)
