#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates
import folium
from folium import plugins


# In[3]:


from pyIUDX.cat import cat
# Specify the catalogue server details.
# initialize a catalogue class
cat = cat.Catalogue("https://varanasi.iudx.org.in/catalogue/v1")


# In[16]:


geo1 = {"circle": {"lat": 25.3176, "lon": 82.9739, "radius": 300000}}
attributes = {"tags": ["dustbin"]}
filters = ["id"]

all_bins_ItemsByID = cat.getManyResourceItems(attributes, filters, geo=geo1)
print(all_bins_ItemsByID[0])
print("Number of items = ", len(all_bins_ItemsByID))


# In[18]:


# Import the item class from pyIUDX.rs
from pyIUDX.rs import item
m = folium.Map(location=[25.3176, 82.9739],zoom_start=12)
plugins.ScrollZoomToggler().add_to(m)
bins = item.Items("https://varanasi.iudx.org.in/catalogue/v1", "https://rs.varanasi.iudx.org.in/resource-server/vscl/v1", all_bins_ItemsByID)
print(bins[0].geoProperties)
for sensor in bins:
  sensor_id = sensor.id  
#   print("Sensor location = ", sensor.location.coordinates)
  folium.Marker([sensor.location.coordinates[1], sensor.location.coordinates[0] ], popup=sensor_id).add_to(m)    
m


# In[19]:


print(bins[0].quantitativeProperties)


# In[20]:


bins.during("2020-01-02T00:00:00.000+05:30", "2020-01-04T00:00:00.000+05:30")


# In[23]:


import matplotlib.pyplot as plt
fig = plt.figure(figsize=(15,10))
fig.suptitle(bins[0].FilledLevel.name + "\n" + bins[0].FilledLevel.describes, fontsize=20)
plt.xlabel(bins[0].timeProperty, fontsize=18)
# plt.ylabel(bins[0].FilledLevel.name + " (" + a[0].PM10_MAX.symbol + ")", fontsize=16)

print(bins[0].FilledLevel.value)
# for sensor in bins[0:10]:
#   plt.plot(sensor.FilledLevel.value[:,0], sensor.FilledLevel.value[:,1], label=sensor.id.split("/")[-1])
# plt.legend()
# plt.show()


# In[ ]:




