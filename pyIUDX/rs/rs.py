import requests
import json


class ResourceServer():
    def __init__(self, rsUrl, cert=None, key=None):
        """Resource serer base class constructor

        Args:
            rsUrl (string): Domain name/ip of the resource server
            cert (string): Absolute Location of cert file
            key (string): Absolute Location of key file

        Raises:
            RuntimeError: If resource server is not reachable
        """
        self.rsUrl = rsUrl
        self.cert = None
        if cert is not None and key is not None:
            self.cert = (cert, key)

        # opts_file = pkg_resources.resource_filename("pyIUDX", "rs/opts.json")
        # """ TODO: see if import works when on pip """
        # with open(opts_file, "r") as f:
        #     self.optsSchema = json.load(f)

    def dispParams(self):
        """ Display rs initalization parameter

        Returns:
            (rsDomain, rsPort, rsVersion) (string, string, string): version string
        """
        return self._rsDomain, self._rsPort, self._rsVersion

    def getUrl(self):
        """ Get rs constructed url

        Returns:
            url (string): rs constructed url
        """
        return (self._rsDomain + ":" + self._rsPort +
                "/resource-server" + "/v" + self._rsVersion)

    def search(self, url, data):
        """ Use requests library to make a search request

        Returns:
            resp (object): Response body
        """
        url = url + "/search"
        headers = {"Content-Type": "application/json"}
        return requests.post(url, data=json.dumps(data),
                             headers=headers, cert=self.cert)

    def download(self, url, data):
        """ Use requests library to make a search request

        Returns:
            resp (object): Response body
        """
        url = url + "/download"
        headers = {"Content-Type": "application/json"}
        return requests.post(url, data=json.dumps(data),
                             headers=headers, cert=self.cert)


    def downloadData(self, groupId, opts=None, token=None):
        """Download data from a resource server

        An optional options dictionary can be passed to
        get more specific data.
        The options dictionary follows the schema:
        https://raw.githubusercontent.com/iudx/pyIUDX/rs/pyIUDX/rs/opts.json

        Args:
            groupId (string): id of the resource item
            opts (Dict): dictionary of various options
        Returns:
            url (string): rs constructed url
        """
        opts = {"options": "all"}
        idDict = {"resourceServerGroup": groupId}
        if token is not None:
            tokenDict = {"token": token}
            data = {**idDict, **opts, **tokenDict}
        else:
            data = {**idDict, **opts}
        resp = self.download(self.rsUrl, data)
        if resp.status_code == 400:
            raise Warning("Bad request. Check query body")
        if resp.status_code == 429:
            raise Warning("Too many requests")
        if resp.status_code == 401:
            raise Warning("Invalid credentials")
        if resp.status_code == 416:
            raise Warning("Query exceeds time limit")
        if resp.status_code == 200:
            return resp.json()

    def getData(self, id, opts=None, token=None):
        """Get data from a resource server

        An optional options dictionary can be passed to
        get more specific data.
        The options dictionary follows the schema:
        https://raw.githubusercontent.com/iudx/pyIUDX/rs/pyIUDX/rs/opts.json

        Args:
            id (string): id of the resource item
            opts (Dict): dictionary of various options
        Returns:
            url (string): rs constructed url
        """
        idDict = {"id": id}
        if token is not None:
            tokenDict = {"token": token}
            data = {**idDict, **opts, **tokenDict}
        else:
            data = {**idDict, **opts}
        resp = self.search(self.rsUrl, data)
        if resp.status_code == 400:
            raise Warning("Bad request. Check query body")
        if resp.status_code == 429:
            raise Warning("Too many requests")
        if resp.status_code == 401:
            raise Warning("Invalid credentials")
        if resp.status_code == 416:
            raise Warning("Query exceeds time limit \n" + json.dumps(resp.json()))
        if resp.status_code == 200:
            return resp.json()

    def getLatestData(self, id, token=None):
        """ Get latest data

        Args:
            id (string): id of the resource item

        Returns:
            data (List[Dict]): Array with a single dictionary
                                item corresponding to the data
        """
        opts = {"options": "latest"}
        return self.getData(id, opts, token)

    def getDataDuring(self, id, startTime, endTime, token=None):
        """Get data during a time interval

        Args:
            id (string): id of the resource item
            startTime (string): Starting from
            endTime (string): Till

        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                                item corresponding to the data
        """
        timeString = startTime + "/" + endTime
        opts = {"TRelation": "during", "time": timeString}
        return self.getData(id, opts, token)


    def getDataBefore(self, id, time, token=None):
        """Get data before a given time

        Args:
            id (string): id of the resource item
            time (string): Ending at

        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                                item corresponding to the data
        """
        opts = {"TRelation": "before", "time": time}
        return self.getData(id, opts, token)

    def getDataAfter(self, id, time, token=None):
        """Get data after a given time

        Args:
            id (string): id of the resource item
            time (string): Starting from

        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                                item corresponding to the data
        """
        opts = {"TRelation": "after", "time": time}
        return self.getData(id, opts, token)

    def getDataAroundDuring(self, id, point, radius, startTime, endTime, token=None):
        """Get data around a specific point(lat, lon) and radius(meters) and during a time

        Args:
            id (string): id of the resource item
            point (List[Float]): point [lat, lon]
            radius (int): radius in meters
            startTime (string): Starting from
            endTime (string): Till

        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                                item corresponding to the data
        """
        timeString = startTime + "/" + endTime
        opts = {"lat": str(point[0]), "lon": str(point[1]),
                "radius": str(radius), "TRelation": "during",
                "time": timeString}
        return self.getData(id, opts, token)

    def getLatestDataAround(self, id, point, radius, token=None):
        """Get data around a specific point(lat, lon) and radius(meters)

        Args:
            id (string): id of the resource item
            point (List[Float]): point [lat, lon]
            radius (int): radius in meters

        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                                item corresponding to the data
        """
        opts = {"lat": str(point[0]), "lon": str(point[1]),
                "radius": str(radius)}
        return self.getData(id, opts, token)

    def getLatestDataAroundLike(self, id, point, radius, attributeName, attributeValue, token=None):
        """Get data around a specific point(lat, lon) and radius(meters)            which has an attribute like

        Args:
            id (string): id of the resource item
            point (List[Float]): point [lat, lon]
            radius (int): radius in meters

        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                                item corresponding to the data
        """
        opts = {"lat": str(point[0]), "lon": str(point[1]),
                "radius": str(radius),
                "comparison-operator": "propertyisequalto",
                "attribute-name": attributeName,
                "attribute-value": attributeValue}
        return self.getData(id, opts, token)

    def getDataValuesLikeDuring(self, id, attribute, val, startTime, endTime, token=None):
        """Get data of an item for which an attribute is like value between a time

        Args:
            id (string): id of the resource item
            attribute (string): attribute name
            val (string): value

        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                                item corresponding to the data
        """
        timeString = startTime + "/" + endTime
        opts = {"attribute-name": attribute,
                "TRelation": "during",
                "time": timeString,
                "attribute-value": val,
                "comparison-operator": "propertyisequalto",
                "startTime": startTime,
                "endTime": endTime}
        return self.getData(id, opts, token)


    def getLatestDataValuesLike(self, id, attribute, val, token=None):
        """Get latest data of an item for which an attribute is like value

        Args:
            id (string): id of the resource item
            attribute (string): attribute name
            val (string): value

        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                                item corresponding to the data
        """
        opts = {"attribute-name": attribute,
                "attribute-value": val,
                "comparison-operator": "propertyisequalto",
                "options": "latest"}
        return self.getData(id, opts, token)

    def getDataValuesGreater(self, id, attribute, minVal, token=None):
        """Get data of an item for which an attribute is greater than minVal

        Args:
            id (string): id of the resource item
            attribute (string): attribute name
            minVal (float): minimum value

        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                                item corresponding to the data
        """
        opts = {"attribute-name": attribute,
                "attribute-value": str(minVal),
                "comparison-operator": "propertyisgreaterthanorequalto",
                "options": "latest"}
        return self.getData(id, opts, token)

    def getDataValuesLesser(self, id, attribute, maxVal, token=None):
        """Get data of an item for which an attribute is lesser than maxVal

        Args:
            id (string): id of the resource item
            attribute (string): attribute name
            maxVal (float): maximum value

        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                                item corresponding to the data
        """
        opts = {"attribute-name": attribute,
                "attribute-value": str(maxVal),
                "comparison-operator": "propertyislessthanorequalto",
                "options": "latest"}
        return self.getData(id, opts, token)

    def getDataValuesBetween(self, id, attribute, minVal, maxVal, token=None):
        """Get data of an item for which an attribute is between minVal and maxVal

        Args:
            id (string): id of the resource item
            attribute (string): attribute name
            minVal (float): minimum value
            maxVal (float): maximum value

        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                               item corresponding to the data
        """
        opts = {"attribute-name": attribute,
                "attribute-value": str(minVal) + "," + str(maxVal),
                "comparison-operator": "propertyisbetween"}
        print(opts)
        return self.getData(id, opts, token)


    def getStatus(self, id, token=None):
        """Get Status of a resource item

        Args:
            id (string): id of the resource item

        Returns:
            status (bool): True if up
        TODO:
        """
        opts = {"options": "status"}
        resp = self.getData(id, opts, token)
        if resp[0]["status"] == "down":
            return False
        else:
            return True
