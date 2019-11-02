from multiprocessing import Pool, Manager
from collections import MutableSequence
from pyIUDX.rs import rs
from pyIUDX.cat import cat
from pyIUDX.auth import auth
import numpy as np
import requests
import copy



""" TODO: FIx numpy datetime issue """
""" TODO: Multiprocessing """
""" TODO: GeoAttributes coming in data """
""" TODO: Read base schemas locally """
""" TODO: Remove cat url in Item() """
""" TODO: Error in case data is not coming """


class QuantitativeProperty(object):
    def __init__(self, obj, name, properties):
        self.name = name
        self.value = np.empty((0, 2), dtype=object)
        for p in properties.keys():
            setattr(self, p, properties[p])
        self.attributes = copy.deepcopy(self.__dict__)
        self.attributes.pop("$ref", None)
        self.attributes.pop("value", None)
        self.attributes.pop("attributes", None)
        self.parent = obj

    def reset(self):
        self.value = np.empty((0, 2), dtype=object)
        return

    def setValue(self, time, value):
        self.value = np.append(self.value,
                               np.array([[time, value]], dtype=object), axis=0)
        return

    def latest(self):
        self.parent.latest()
        return self.value

    def valueBetween(self, minval, maxVal):
        self.parent.valueBetween(self.name, minval, maxVal)
        return self.value


class GeoProperty(object):
    def __init__(self, geoProperty):
        if geoProperty["value"]["geometry"]["type"] == "Point":
            self.type = "Point"
            self.coordinates = geoProperty["value"]["geometry"]["coordinates"]
        elif geoProperty["value"]["geometry"]["type"] == "Polygon":
            self.type = "Polygon"
            self.coordinates = geoProperty["value"]["geometry"]["coordinates"]


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
        self.rs = rs.ResourceServer("https://pudx.resourceserver.iudx.org.in/resource-server/pscdcl/v1")

        """ Item Objects """
        self.id = resourceItemId
        cat_item = self.cat.getOneResourceItem(self.id)
        if cat_item is None:
            raise RuntimeError("Item :" + self.id +
                               " not found in catalogue")

        geoAttributes = []
        self.timeAttributes = []
        self.quantitativeAttributes = []

        for key in cat_item.keys():
            if isinstance(cat_item[key], dict):
                if cat_item[key]["type"] == "GeoProperty":
                    geoAttributes.append(key)

        """ TODO: What if there is more than one geoProperty """
        self.geoAttributes = geoAttributes[0]
        setattr(self, self.geoAttributes, GeoProperty(cat_item[self.geoAttributes]))

        """ Load datamodel properties """
        try:
            self.dm = requests.get(cat_item["refDataModel"]["value"]).json()
        except Exception as e:
            raise RuntimeError("Couldn't retrieve item's data model")

        """ TODO: Geoproperty in data model """
        for attr in self.dm["properties"].keys():
            attrType = self.dm["properties"][attr]["$ref"].split("/")[-1]
            if attrType == "TimeProperty":
                self.timeAttributes.append(attr)
            if attrType == "QuantitativeProperty":
                self.quantitativeAttributes.append(attr)
                setattr(self, attr,
                        QuantitativeProperty(self, attr, self.dm["properties"][attr]))

        """ TODO: What if multiple time attributes """
        self.timeAttribute = self.timeAttributes[0]

    def reset(self):
        """ Reset data of all quantitative attributes of this item
        Returns:
            self (object): Returns back the updated object
        """
        for d in self.quantitativeAttributes:
            getattr(self, d).reset()

    def populateValue(self, data):
        for row in data:
            timestamp = row[self.timeAttribute]
            for k in row.keys():
                if k in self.quantitativeAttributes:
                    try:
                        getattr(self, k).setValue(timestamp, float(row[k]))
                    except Exception as e:
                        pass

    def latest(self):
        """ Get latest data for an item
        Returns:
            self (object): Returns back the updated object
        """
        data = self.rs.getLatestData(self.id)
        self.reset()
        self.populateValue(data)
        return self

    def during(self, start, end):
        self.reset()
        data = self.rs.getDataDuring(self.id, start, end)
        self.populateValue(data)
        return self

    def valueBetween(self, attrName, minval, maxVal):
        self.reset()
        data = self.rs.getDataValuesBetween(self.id, attrName, minval, maxVal)
        self.populateValue(data)


    """ TODO: Add Status """


class Items(MutableSequence):
    def __init__(self, catUrl, items=None):
        super(Items, self).__init__()
        self.list = Manager().list()
        self.catUrl = catUrl
        if items is None:
            return

        """ Init items """
        with Pool(4) as p:
            p.starmap(self.initItem, [(self.catUrl, item["id"], self.list) for item in items])
            p.close()
            p.join()
        self.list = list(self.list)
        self.len = len(self.list)

    def initItem(self, catUrl, item, objList):
        objList.append(Item(catUrl, item))

    def getLatest(self, obj):
        obj.latest()
        return obj

    def getDuring(self, obj, startTime, endTime):
        obj.during(startTime, endTime)
        return obj

    def latest(self):
        with Pool(4) as p:
            self.list = p.map(self.getLatest, self.list)
            p.close()
            p.join()

    def during(self, startTime, endTime):
        with Pool(4) as p:
            self.list = p.starmap(self.getDuring,
                                  [(self.list[i], startTime, endTime,)
                                      for i in range(self.len)])
            p.close()
            p.join()

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self.list)

    def __len__(self):
        """List length"""
        return len(self.list)

    def __getitem__(self, ii):
        """Get a list item"""
        return self.list[ii]

    def __delitem__(self, ii):
        """Delete an item"""
        del self.list[ii]

    def __setitem__(self, ii, val):
        self.list[ii] = val

    def __str__(self):
        return str(self.list)

    def insert(self, ii, val):
        self.list.insert(ii, val)
