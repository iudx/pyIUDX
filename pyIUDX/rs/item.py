from pyIUDX.rs import rs
from pyIUDX.cat import cat
import numpy as np
import urllib3
import requests
import copy
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


""" TODO: FIx numpy datetime issue """
""" TODO: Multiprocessing """
""" TODO: GeoAttributes coming in data """
""" TODO: Read base schemas locally """


class QuantitativeProperty(object):
    def __init__(self, properties):
        self.value = np.empty((0, 2), dtype=object)
        for p in properties.keys():
            setattr(self, p, properties[p])
        self.attributes = copy.deepcopy(self.__dict__)
        self.attributes.pop("$ref", None)
        self.attributes.pop("value", None)
        self.attributes.pop("attributes", None)

    def reset(self):
        self.value = np.empty((0, 2), dtype=object)

    def setValue(self, time, value):
        self.value = np.append(self.value,
                               np.array([[time, value]], dtype=object), axis=0)


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
        self.rs = rs.ResourceServer("https://pune.iudx.org.in/resource-server/pscdcl/v1")

        """ Item Objects """
        self.riId = resourceItemId
        cat_item = self.cat.getOneResourceItem(self.riId)
        if cat_item is None:
            raise RuntimeError("Item :" + self.riId +
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
                        QuantitativeProperty(self.dm["properties"][attr]))

    def reset(self):
        """ Reset data of all quantitative attributes of this item
        Returns:
            self (object): Returns back the updated object
        """
        for d in self.quantitativeAttributes:
            getattr(self, d).reset()

    def latest(self):
        """ Get latest data for an item
        Returns:
            self (object): Returns back the updated object
        """
        data = self.rs.getLatestData(self.riId)[0]
        """ TODO: Workaround for [0] below """
        timeAttr = list(set(self.timeAttributes).intersection(set(data.keys())))[0]
        timestamp = data[timeAttr]
        self.reset()
        for d in data.keys():
            if d in self.quantitativeAttributes:
                try:
                    getattr(self, d).setValue(timestamp, float(data[d]))
                except Exception as e:
                    pass
        return self

    def during(self, start, end):
        self.reset()
        data = self.rs.getDataDuring(self.riId, start, end)
        for row in data:
            timeAttr = list(set(self.timeAttributes).intersection(set(row.keys())))[0]
            timestamp = row[timeAttr]
            for k in row.keys():
                if k in self.quantitativeAttributes:
                    try:
                        getattr(self, k).setValue(timestamp, float(row[k]))
                    except Exception as e:
                        return None
        return self


class Items(object):
    def __init__(self):
        pass
