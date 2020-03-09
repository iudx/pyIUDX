import requests
import json


class Item():
    def __init__(self, item_id, token=None, cert=None, key=None):
        """Resource serer base class constructor

        Args:
            item_id (string): id of the item
            cert (string): Absolute Location of cert file
            key (string): Absolute Location of key file

        Raises:
            RuntimeError: If resource server is not reachable
        """
        self.item_id = item_id
        """ TODO: Remove hardcoding later """
        self._rsUrl = "https://" + item_id.split("/")[2] + "/resource-server/vscl/v1"
        print(self._rsUrl)
        self._cert = (cert, key)
        self._token = token
        self._opts = {}

        # opts_file = pkg_resources.resource_filename("pyIUDX", "rs/opts.json")
        # """ TODO: see if import works when on pip """
        # with open(opts_file, "r") as f:
        #     self.optsSchema = json.load(f)

    def dispParams(self):
        """ Display rs initalization parameter
        Returns:
            (rsUrl) (string): version string
        """
        return self._rsUrl


    def search(self, data):
        """ Use requests library to make an IUDX search request
        Returns:
            resp (object): Response body
        """
        url = self._rsUrl + "/search"
        headers = {"Content-Type": "application/json"}
        return requests.post(url, data=json.dumps(data),
                             headers=headers, cert=self._cert)

    def download(self, data):
        """ Use requests library to make an IUDX data download request

        Returns:
            resp (object): Response body
        """
        url = self._rsUrl + "/download"
        headers = {"Content-Type": "application/json"}
        return requests.post(self._rsUrl, data=json.dumps(data),
                             headers=headers, cert=self._cert)



    def get(self):
        """Get data from a resource server

        An optional options dictionary can be passed to
        get more specific data.
        The options dictionary follows the schema:
        https://raw.githubusercontent.com/iudx/pyIUDX/rs/pyIUDX/rs/opts.json

        Args:
            opts (Dict): dictionary of various options
        Returns:
            data (Dict): Output JSON data
        """
        idDict = {"id": self.item_id}
        if self._token is not None:
            tokenDict = {"token": self._token}
            data = {**idDict, **self._opts, **tokenDict}
        else:
            data = {**idDict, **self._opts}
        resp = self.search(data)
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

    def latest(self):
        """Get latest data

        Returns:
            self (Object):  self
        """
        opts = {"options": "latest"}
        self._opts = {**self._opts, **opts}
        return self

    def during(self, startTime, endTime):
        """Get data during a time interval

        Args:
            startTime (string): Starting from
            endTime (string): Till

        TODO: 
            Validate time

        Returns:
            self (Object):  self
        """
        timeString = startTime + "/" + endTime
        opts = {"TRelation": "during", "time": timeString}
        self._opts = {**self._opts, **opts}
        return self

    def before(self, time):
        """Get data before a given time

        Args:
            time (string): Ending at

        TODO: 
            Validate time

        Returns:
            self (Object):  self
        """
        opts = {"TRelation": "before", "time": time}
        self._opts = {**self._opts, **opts}
        return self

    def after(self, time):
        """Get data after a given time

        Args:
            time (string): Starting from

        TODO: 
            Validate time

        Returns:
            self (Object):  self
        """
        opts = {"TRelation": "after", "time": time}
        self._opts = {**self._opts, **opts}
        return self

    def around(self, point, radius):
        """Get data around a specific point(lat, lon) and radius(meters)

        Args:
            point (List[Float]): point [lat, lon]
            radius (int): radius in meters

        Returns:
            self (Object):  self
        """
        timeString = startTime + "/" + endTime
        opts = {"lat": str(point[0]), "lon": str(point[1]),
                "radius": str(radius), "TRelation": "during",
                "time": timeString}
        self._opts = {**self._opts, **opts}
        return self


    def like(self, attribute, val):
        """Get latest data of an item for which an attribute is like value

        Args:
            attribute (string): attribute name
            val (string): value

        Returns:
            self (Object):  self
        """
        opts = {"attribute-name": attribute,
                "attribute-value": val,
                "comparison-operator": "propertyisequalto",
                "options": "latest"}
        self._opts = {**self._opts, **opts}
        return self

    def greater(self, attribute, minVal):
        """Get data of an item for which an attribute is greater than minVal

        Args:
            id (string): id of the resource item
            attribute (string): attribute name
            minVal (float): minimum value

        Returns:
            self (Object):  self
        """
        opts = {"attribute-name": attribute,
                "attribute-value": str(minVal),
                "comparison-operator": "propertyisgreaterthanorequalto",
                "options": "latest"}
        self._opts = {**self._opts, **opts}
        return self

    def lesser(self, attribute, maxVal):
        """Get data of an item for which an attribute is lesser than maxVal

        Args:
            attribute (string): attribute name
            maxVal (float): maximum value

        Returns:
            self (Object):  self
        """
        opts = {"attribute-name": attribute,
                "attribute-value": str(maxVal),
                "comparison-operator": "propertyislessthanorequalto",
                "options": "latest"}
        self._opts = {**self._opts, **opts}
        return self

    def between(self, attribute, minVal, maxVal):
        """Get data of an item for which an attribute is between minVal and maxVal

        Args:
            attribute (string): attribute name
            minVal (float): minimum value
            maxVal (float): maximum value

        Returns:
            self (Object):  self
        """
        opts = {"attribute-name": attribute,
                "attribute-value": str(minVal) + "," + str(maxVal),
                "comparison-operator": "propertyisbetween"}
        self._opts = {**self._opts, **opts}
        return self


    def status(self):
        """Get Status of a resource item

        Args:
            id (string): id of the resource item

        Returns:
            status (bool): True if up
        TODO:
        """
        opts = {"options": "status"}
        resp = self.getData(opts)
        if resp[0]["status"] == "down":
            return False
        else:
            return True
