from multiprocessing import Pool, Manager
from collections import MutableSequence
from pyIUDX.rs import rs
from pyIUDX.cat import cat
from pyIUDX.auth import auth
import numpy as np
import datetime
import requests
import copy



""" TODO: FIx numpy datetime issue """
""" TODO: GeoAttributes coming in data """
""" TODO: Read base schemas locally """
""" TODO: Remove cat url in Item() """
""" TODO: Error in case data is not coming """
""" TODO: Item constructor can directly take catalogue entry """


class Property(object):
    """Container class for a Property

    Property is an aspect of a resource item that describes it
    or its current value
    """

    def __init__(self, name, properties):
        self.name = name
        self.value = None
        for p in properties.keys():
            setattr(self, p, properties[p])
        self.attributes = copy.deepcopy(self.__dict__)
        self.attributes.pop("$ref", None)
        self.attributes.pop("attributes", None)

    def setValue(self,  value, time=None):
        """Set State for this Property
        Args:
            value (string): Value
            time (datetime.datetime()): Time index
        """
        if time is None:
            self.value = value
        else:
            self.value = np.append(self.value,
                                   np.array([[time, value]],
                                            dtype=object), axis=0)
        return

    def reset(self):
        if isinstance(self.value, str):
            return
        self.value = np.empty((0, 2), dtype=object)

    def sort(self):
        """Sort time series
        """
        self.value = self.value[np.argsort(self.value[:, 0])]


class QuantitativeProperty(object):
    """Container class for a quantitative property
    QuantitativeProperty is a measureable property having
    further attributes such as units. Values are always indexed
    with time.
    """

    def __init__(self, obj, name, properties):
        """QuantitativeProperty constructor
        Args:
            obj (object): Parent object
            name (string): This property's name
            properties (Dict[string]): Various properties of the QuantitativeProperty
            e.g {"unitText": "ppm", "describes": "description of the property"]
        """
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
        """Reset value of this Property
        """
        self.value = np.empty((0, 2), dtype=object)
        return

    def sort(self):
        """Sort time series
        """
        self.value = self.value[np.argsort(self.value[:, 0])]

    def setValue(self, time, value):
        """Set Value for this Property
        Args:
            time (datetime.datetime()): Time index
            value (float): Value
        """
        try:
            value = float(value)
            self.value = np.append(self.value,
                                   np.array([[time, value]], dtype=object),
                                   axis=0)
        except:
            pass
        return

    def latest(self):
        """Get latest data for this property
        Returns:
            value (ndarray): numpy 2d array with 0th column as time
        """
        self.parent.latest()
        return self.value

    def during(self, startTime, endTime):
        """Get data during a set interval for this property
        Args:
            startTime (string): Start time
            endTime (string): End time
        Returns:
            value (ndarray): numpy 2d array with 0th column as time
        TODO:
            Use date time instead of strings
        """
        self.parent.during(startTime, endTime)
        return self.value

    def valueBetween(self, minval, maxVal):
        """Get all data during which this attribute was between min and max val
        Args:
            minVal (int): minimum value
            minVal (int): maximum value
        Returns:
            value (ndarray): numpy 2d array with 0th column as time
        TODO:
            Specify time frame too
        """
        self.parent.valueBetween(self.name, minval, maxVal)
        return self.value


class GeoProperty(object):
    """Container class for a Geo property
    GeoProperty is a spatial property having
    further attributes such as coordinates for either a point or a polygon.
    """

    def __init__(self, name):
        """GeoProperty constructor

        Properties to be used only for geoProperties defined in dataModels

        Args:
            properties (Dict[string]): Various properties of the GeoProperty
            to bes passed only if this property is defined in data model
        """
        self.name = name
        """ Type in case geoProperty is static """
        self.type = None
        self.coordinates = None

    def setStaticGeo(self, geoProperty):
        """ Static points """
        if geoProperty["value"]["geometry"]["type"] == "Point":
            self.type = "Point"
            self.coordinates = geoProperty["value"]["geometry"]["coordinates"]

        elif geoProperty["value"]["geometry"]["type"] == "Polygon":
            self.type = "Polygon"
            self.coordinates = geoProperty["value"]["geometry"]["coordinates"]

    def setDynamicGeo(self, time, coordinates):
        """Set Value for this geoProperty

        To be used only when this geoProperty is time varying

        Args:
            time (datetime.datetime()): Time index
            value (float): Value
        """
        if isinstance(coordinates, dict):
            try:
                tp = coordinates["type"]
                if tp == "Point":
                    coordinates = coordinates["coordinates"]
            except:
                pass
        elif isinstance(coordinates, str):
            try:
                coordinates = float(coordinates)
            except:
                pass
        elif isinstance(coordinates, float):
            pass

        self.coordinates = np.append(self.coordinates,
                                     np.array([[time, coordinates]],
                                              dtype=object), axis=0)
        return

    def reset(self):
        """Reset coordinates
        This is only invoked in case where this geoProperty is time varying
        TODO: Workaround for type
        """
        if self.type is None:
            self.coordinates = np.empty((0, 2), dtype=object)

    def sort(self):
        """Sort time series
        """
        self.coordinates = self.coordinates[np.argsort(self.coordinates[:, 0])]


class Item(object):
    """class for an iudx resource item

    A resource item has it's static attribute representation in a catalogue
    and a dynamic "data" representation in a resource server.
    This class presents an abstraction layer combining both
    """

    def __init__(self, catUrl, resourceItemId, dataModel=None):
        """ PyIUDX item base class
        Args:
            catUrl (string): Domain name/ip of the catalogue server
        """
        self.id = resourceItemId
        self.cat = cat.Catalogue(catUrl)
        """ TODO: get rs from catalogue item """
        self.rs = rs.ResourceServer("https://pudx.resourceserver.iudx.org.in/resource-server/pscdcl/v1")
        catItem = self.cat.getOneResourceItem(self.id)
        if catItem is None:
            raise RuntimeError("Item :" + self.id +
                               " not found in catalogue")

        self.properties = []
        self.geoProperties = []
        self.timeProperties = []
        self.quantitativeProperties = []

        """ Load datamodel properties """
        self.dm = dataModel
        if self.dm is None:
            try:
                self.dm = self.cat.getDataModel(self.id)
            except Exception as e:
                raise RuntimeError("Couldn't retrieve item's data model")

        """ Read attributes from datamodel and store"""
        for attr in self.dm["properties"].keys():
            try:
                attrType = self.dm["properties"][attr]["$ref"].split("/")[-1]
            except:
                continue

            if attrType == "Property":
                self.properties.append(attr)
                setattr(self, attr,
                        Property(attr,
                                 self.dm["properties"][attr]))

            if attrType == "TimeProperty":
                self.timeProperties.append(attr)

            if attrType == "QuantitativeProperty":
                self.quantitativeProperties.append(attr)
                setattr(self, attr,
                        QuantitativeProperty(self, attr,
                                             self.dm["properties"][attr]))

            if attrType == "GeoProperty":
                self.geoProperties.append(attr)
                setattr(self, attr,
                        GeoProperty(attr))

        """ TODO: What if multiple time attributes """
        """ Find time attribute from datamodel """
        self.timeProperty = self.timeProperties[0]

        """ Read item properties """
        for key in catItem.keys():
            if isinstance(catItem[key], dict):
                if (catItem[key]["type"] == "GeoProperty" and
                        key in self.geoProperties):
                    getattr(self, key).setStaticGeo(catItem[key])
                if (catItem[key]["type"] == "Property" and
                        key in self.properties):
                    getattr(self, key).setValue(catItem[key])

    def populateValue(self, data):
        """Helper function to populate a QuantitativeProperty's value array
        """
        if data is None:
            return
        for row in data:
            """ TODO: Assuming a datetime format is bad """
            timeNoFloat = 0
            try:
                timestamp = datetime.datetime\
                                .strptime(row[self.timeProperty].split("+")[0],
                                          "%Y-%m-%dT%H:%M:%S.%f")
            except:
                timeNoFloat = 1
                pass
            if timeNoFloat == 1:
                try:
                    timestamp = datetime.datetime\
                                    .strptime(row[self.timeProperty].split("+")[0],
                                              "%Y-%m-%dT%H:%M:%S")
                except:
                    continue

            for k in row.keys():
                if k in self.quantitativeProperties:
                    attr = getattr(self, k)
                    attr.setValue(timestamp, row[k])
                if k in self.geoProperties:
                    attr = getattr(self, k)
                    attr.setDynamicGeo(timestamp, row[k])
                if k in self.properties:
                    attr = getattr(self, k)
                    attr.setValue(row[k], time=timestamp)

        """Sort time series """
        for k in self.quantitativeProperties:
            getattr(self, k).sort()
        for k in self.geoProperties:
            pass
            #getattr(self, k).sort()
        for k in self.properties:
            getattr(self, k).sort()

    def reset(self):
        """ Reset data of all quantitative attributes of this item
        Returns:
            self (object): Returns back the updated object
        """
        for d in self.properties:
            getattr(self, d).reset()

        for d in self.quantitativeProperties:
            getattr(self, d).reset()

        for d in self.geoProperties:
            getattr(self, d).reset()

    def latest(self):
        """ Get latest data for all properties belonging to this item

        Returns:
            self (object): Returns back the updated object
        """
        data = self.rs.getLatestData(self.id)
        self.reset()
        self.populateValue(data)
        return self

    def during(self, start, end):
        """Get data during a set interval for all properties belonging to this item

        Args:
            startTime (string): Start time
            endTime (string): End time

        Returns:
            value (ndarray): numpy 2d array with 0th column as time
        """
        data = self.rs.getDataDuring(self.id, start, end)
        self.reset()
        self.populateValue(data)
        return self

    def latestWith(self, attr, val):
        """ Get latest data for all properties belonging to this item with a specific attribute
            
            This method will give latest data where an attribute is specified. For e.g 
            attr = "ROUTE_ID", val = "110" will give latest data for that bus

        Args:
            attr (string): The name of the attribute
            val (string): The value of the attribute

        Returns:
            self (object): Returns back the updated object
        """
        data = self.rs.getLatestDataValuesLike(self.id, attr, val)
        self.reset()
        self.populateValue(data)
        return self


    def valueBetween(self, attrName, minval, maxVal):
        """Get all data during which this attribute was between min and max val

        Args:
            attrName (string): name of the attribute
            minVal (int): minimum value
            minVal (int): maximum value

        TODO:
            Specify time frame too
        """
        data = self.rs.getDataValuesBetween(self.id, attrName, minval, maxVal)
        self.populateValue(data)


    """ TODO: Add Status """


class Items(MutableSequence):
    """class for a list of iudx resource items.

    This class extends a list to provide Class Item style functionality
    coupled with multiprocessing pool to allow for faster data access
    """

    def __init__(self, catUrl, items=None):
        """ PyIUDX items base class

        Args:
            catUrl (string): Domain name/ip of the catalogue server
        """
        super(Items, self).__init__()
        self.list = Manager().list()
        self.catUrl = catUrl
        self.cat = cat.Catalogue(catUrl)
        if items is None:
            return

        """ TODO: Replace this with resourceGroup datamodel """
        """ Get initial datamodel """
        try:
            self.dm = self.cat.getDataModel(items[0]["id"])
        except Exception as e:
            raise RuntimeError("Couldn't retrieve item's data model")

        """ Init items """
        with Pool(4) as p:
            p.starmap(self.initItem, [(self.catUrl, item["id"], self.list) for item in items])
            p.close()
            p.join()
        self.list = list(self.list)
        self.len = len(self.list)

    def initItem(self, catUrl, item, objList):
        """Multiprocessed job """
        objList.append(Item(catUrl, item, self.dm))

    def getLatest(self, obj):
        """Multiprocessed job """
        obj.latest()
        return obj

    def getDuring(self, obj, startTime, endTime):
        """Multiprocessed job """
        obj.during(startTime, endTime)
        return obj

    def latest(self):
        """ Get latest data

        For all resource items of this instance and for all
        properties belonging to this item

        Returns:
            self (object): Returns back the updated object
        """
        with Pool(4) as p:
            self.list = p.map(self.getLatest, self.list)
            p.close()
            p.join()
        return self

    def during(self, startTime, endTime):
        """Get data during a set interval

        For all resource items of this
        instance and for all properties belonging to this item

        Args:
            startTime (string): Start time
            endTime (string): End time

        Returns:
            value (ndarray): numpy 2d array with 0th column as time
        """
        with Pool(4) as p:
            self.list = p.starmap(self.getDuring,
                                  [(self.list[i], startTime, endTime,)
                                      for i in range(self.len)])
            p.close()
            p.join()
        return self

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
