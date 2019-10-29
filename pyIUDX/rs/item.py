from pyIUDX.rs import rs
from pyIUDX.cat import cat
import pyIUDX.auth
import numpy as np
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


""" TODO: FIx numpy datetime issue """
""" TODO: Multiprocessing """


class QuantitativeProperty(object):
    def __init__(self, properties):
        self.attributes = []
        self.value = np.empty((0, 2), dtype=object)
        for p in properties.keys():
            self.attributes.append(p)
            setattr(self, p, properties[p])

    def reset(self):
        self.value = np.empty((0, 2), dtype=object)

    def setValue(self, time, value):
        self.value = np.append(self.value,
                               np.array([[time, value]], dtype=object), axis=0)


class Item(object):
    def __init__(self, catUrl, resourceItemId):
        """ PyIUDX base class
        Args:
            catDomain (string): Domain name/ip of the catalogue server
            catPort (string): Catalogue server port
            catVersion (string): catalogue version
        """
        """ IUDX Objects """
        self.cat = cat.Catalogue(catUrl)
        """ TODO: get rs from catalogue item """
        self.rs = rs.ResourceServer("https://pune.iudx.org.in/resource-server/pscdcl/v1")

        """ Item Objects """
        self.riId = resourceItemId
        cat_item = self.cat.getOneResourceItem(self.riId)
        if cat_item is None:
            raise RuntimeError("Item :" + self.riId +
                               " not found in catalogue")
        try:
            self.dm = requests.get(cat_item["refDataModel"]["value"]).json()
        except Exception as e:
            raise RuntimeError("Couldn't retrieve item's data model")

        self.attributes = []
        self.timeAttributes = []
        self.quantitativeAttributes = []
        for attr in self.dm["properties"].keys():
            self.attributes.append(attr)
            attrType = self.dm["properties"][attr]["$ref"].split("/")[-1]
            if attrType == "TimeProperty":
                self.timeAttributes.append(attr)
            if attrType == "QuantitativeProperty":
                self.quantitativeAttributes.append(attr)
                setattr(self, attr,
                        QuantitativeProperty(self.dm["properties"][attr]))

    def reset(self):
        for d in self.quantitativeAttributes:
            getattr(self, d).reset()

    def latest(self):
        data = self.rs.getLatestData(self.riId)[0]
        """ TODO: Workaround for [0] below """
        timeAttr = list(set(self.timeAttributes).intersection(set(data.keys())))[0]
        timestamp = data[timeAttr]
        self.reset()
        for d in data.keys():
            if d in self.quantitativeAttributes:
                getattr(self, d).setValue(timestamp, float(data[d]))
        return self

    def during(self, start, end):
        self.reset()
        data = self.rs.getDataDuring(self.riId, start, end)
        for row in data:
            timeAttr = list(set(self.timeAttributes).intersection(set(row.keys())))[0]
            timestamp = row[timeAttr]
            for k in row.keys():
                if k in self.quantitativeAttributes:
                    getattr(self, k).setValue(timestamp, float(row[k]))


