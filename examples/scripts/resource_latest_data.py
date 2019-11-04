""" Get latest data available for a particular resource identified by its ID from PUDX resource server

An example python script to give the latest data available for a particular resource from the PUDX resource server
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

"""Get the latest data for the particular resource ID from the PUDX resource server
"""
latestData = resource.getLatestData(id)
print(latestData)
