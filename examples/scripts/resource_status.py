""" Get status of a particular resource from PUDX resource server by its ID

An example python script to give the status of a resource from the PUDX resource server by using the resource ID
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

"""Get the status for the particular resource ID from the PUDX resource server
"""
status = resource.getStatus(id)
print(status)
