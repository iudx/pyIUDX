import sys
sys.path.insert(1, '../pyIUDX')
from pyIUDX.rs import item

aqm = item.Item("https://catalogue.iudx.org.in/catalogue/v1", "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pscdcl/aqm-bosch-climo/Pune Railway Station_28")

""" Print aqm item's time attributes """
print(aqm.timeAttributes)
""" Print aqm item's geo attributes """
print(aqm.geoAttributes)
""" Print aqm item's geo attributes type and coordinates"""
print(aqm.location.type)
print(aqm.location.coordinates)

""" Print aqm item's quantitativeAttributes attributes """
print(aqm.quantitativeAttributes)
""" Print CO2 units and subattributes """
print(aqm.UV_MAX.unitText)
print(aqm.CO2_MIN.symbol)
print(aqm.CO2_MIN.attributes)

""" Get latest data for aqm and print Humidity """
print(aqm.latest().HUMIDITY.value)
""" Print latest CO2_MAX value, latest() was already done """
# print(aqm.CO2_MAX.value)

""" Get data during time period for that aqm device """
aqm.during("2019-10-18T00:00:00.000Z", "2019-10-19T00:00:00.000Z")
""" Print its values, numpy array """
# print(aqm.CO2_MAX.value)
