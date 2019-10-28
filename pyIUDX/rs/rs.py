import urllib3
import requests
import pkg_resources
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ResourceServer():
    def __init__(self, rsUrl):
        """Resource serer base class constructor
        Args:
            rsUrl (string): Domain name/ip of the resource server
        Raises:
            RuntimeError: If resource server is not reachable
        """
        self.rsUrl = rsUrl

        opts_file = pkg_resources.resource_filename("pyIUDX", "rs/opts.json")
        """ TODO: see if import works when on pip """
        with open(opts_file, "r") as f:
            self.optsSchema = json.load(f)

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
        return requests.post(url, data=json.dumps(data), headers=headers)

    def getData(self, id, opts=None):
        """ Get data from rs
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
        data = {**idDict, **opts}
        resp = self.search(self.rsUrl, data)
        if resp.status_code == 400:
            raise Warning("Bad request. Check query body")
            return []
        if resp.status_code == 429:
            raise Warning("Too many requests")
            return []
        if resp.status_code == 401:
            raise Warning("Invalid credentials")
            return []
        if resp.status_code == 200:
            return resp.json()

    def getLatestData(self, id):
        """ Get latest data
        Args:
            id (string): id of the resource item
        Returns:
            data (List[Dict]): Array with a single dictionary
                                item corresponding to the data
        """
        opts = {"options": "latest"}
        return self.getData(id, opts)

    def getDataDuring(self, id, startTime, endTime):
        """ Get data during a time interval
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
        return self.getData(id, opts)

    def getDataBefore(self, id, time):
        """ Get data before a given time
        Args:
            id (string): id of the resource item
            time (string): Ending at
        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                                item corresponding to the data
        """
        opts = {"TRelation": "before", "time": time}
        return self.getData(id, opts)

    def getDataAfer(self, id, time):
        """ Get data after a given time
        Args:
            id (string): id of the resource item
            time (string): Starting from
        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                                item corresponding to the data
        """
        opts = {"TRelation": "after", "time": time}
        return self.getData(id, opts)

    def getDataAround(self, id, point, radius):
        """ Get data around a specific point(lat, lon) and radius(meters)
        Args:
            id (string): id of the resource item
            point (List[String]): point [lat, lon]
            radius (int): radius in meters
        Returns:
            data (List[Dict]): Array with a time indexed dictionary
                                item corresponding to the data
        """
        opts = {"lat": str(point[0]), "lon": str(point[1]),
                "radius": str(radius)}
        return self.getData(id, opts)

    def getStatus(self, id):
        """ Get Status of a resource item
        Args:
            id (string): id of the resource item
        Returns:
            status (bool): True if up
        """
        opts = {"options": "status"}
        resp = self.getData(id, opts)
        if resp[0]["status"] == "down":
            return False
        else:
            return True
