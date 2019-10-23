import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Catalogue():
    def __init__(self, catDomain, catPort, catVersion="1"):
        """Catalogue base class constructor
        Args:
            catDomain (string): Domain name/ip of the catalogue server
            catPort (string): Catalogue server port
            catVersion (string): catalogue version
        Raises:
            RuntimeError: If catalogue server is not reachable
        """
        self._catDomain = None
        self._catPort = None
        self._catVersion = None
        self._catDomain = catDomain
        self._catPort = catPort
        self._catVersion = catVersion

    def checkConnection(self):
        url = (self._catDomain + ":" + self._catPort +
               "/catalogue" + "/v" + self._catVersion + "/count")
        connect = requests.get(url)
        if connect.status_code != 200:
            raise RuntimeError("Couldn't connect to catalogue server")

    def dispParams(self):
        """ Display catalogue initalization parameter
        Returns:
            (catDomain, catPort, catVersion) (string, string, string): version string
        """
        return self._catDomain, self._catPort, self._catVersion

    def getUrl(self):
        """ Get catalogue constructed url
        Returns:
            url (string): catalogue constructed url
        """
        return (self._catDomain + ":" + self._catPort +
                "/catalogue" + "/v" + self._catVersion)

    def getAllItems(self):
        """ Get all catalogue items
        Returns:
            list (List[Dict]): List  of catalogue items (dicts)
        """
        url = self.getUrl() + "/search"
        items = requests.get(url)
        return(items.json())

    def makeOpts(self, attributes=None, filters=None, geo=None):
        """ Make attributes options string
        Args:
            attributes (Dict): Array of key value pairs
                                     For e.x,
                                     {"tags": ["a", "b"], "provider": ["c"]}
            filters (List[str]): Array of strings as filter opts
                                     For e.x,
                                     ["id", "provider"]
        Returns:
            opts (string): options as a string for a GET method
        """
        opts = ""
        attrOpts = ""
        attrKeys = []
        attrValues = []
        filterOpts = ""
        geoOpts = ""
        if attributes is not None:
            for attr in attributes.keys():
                attrKeys.append(attr)
                attrValues.append(attributes[attr])
            attrOpts = ("attribute-name=(" + ",".join(a for a in attrKeys) + ")&" +
                        "attribute-value=(" +
                        "".join(str(tuple(a)).replace("\'", "")
                                for a in attrValues) + ")")
        if filters is not None:
            filterOpts = ("attribute-filter=" +
                          str(tuple(filters)).replace("\'", ""))

        if geo is not None:
            geoKeys = list(geo.keys())
            if len(geoKeys) is not 1:
                raise RuntimeError("Multiple Geo Options not supported")
            geoKey = geoKeys[0]

            try:
                if geoKey is "circle":
                    geoOpts = ("lat=" + str(geo[geoKey]["lat"]) + "&" +
                               "lon=" + str(geo[geoKey]["lon"]) + "&" +
                               "radius=" + str(geo[geoKey]["radius"]))

                if geoKey is "polygon":
                    if geo[geoKey][0] != geo[geoKey][-1]:
                        raise RuntimeError("Last point not equal to first point")
                    geoOpts = ("geometry=polygon(" +
                               ",".join(str(g[0]) + "," + str(g[1])
                                        for g in geo[geoKey]) + ")" +
                               "&relation=within")

                if geoKey is "bbox":
                    if len(geo[geoKey]) != 2:
                        raise RuntimeError("Two points needed for bbox query")
                    geoOpts = ("bbox=" +
                               ",".join(str(g[0]) + "," + str(g[1])
                                        for g in geo[geoKey]) +
                               "&relation=within")

                if geoKey is "line":
                    geoOpts = ("geometry=linestring(" +
                               ",".join(str(g[0]) + "," + str(g[1])
                                        for g in geo[geoKey]) + ")" +
                               "&relation=intersects")

                opts = (attrOpts +
                        ("&" if attributes is not None else "") + filterOpts +
                        ("&" if filters is not None else "") + geoOpts)

            except Exception as e:
                raise RuntimeError("Incorrect parameter given.\n", e)

        return opts

    def getItemCount(self, attributes=None, filters=None, geo=None):
        """ Number of items matching the criterion
        Args:
            attributes (Dict): Array of key value pairs
                                     For e.x,
                                     {"tags": ["a", "b"], "provider": ["c"]}
            filters (List[str]): Array of strings as filter opts
                                     For e.x,
                                     ["id", "provider"]
        Returns:
            count (int): number of items or -1 if fail
        """
        url = self.getUrl() + "/count"
        opts = self.makeOpts(attributes, filters, geo)
        url = url + "?" + opts
        count = requests.get(url)
        if count.status_code is 200:
            return count.json()["Count"]
        else:
            return -1

    def getOneResourceItem(self, id, filters=None):
        """ Item given the id
        Args:
            id (string): ID of the resourceItem
            filters (List[str]): Array of strings as filter opts
                                     For e.x,
                                     ["id", "provider"]
        Returns:
            list (List[Dict]): List  of catalogue items (dicts)
        """
        url = self.getUrl() + "/items" + "/" + id
        opts = self.makeOpts(None, filters)
        url = url + "?" + opts
        item = requests.get(url)
        if item.status_code is 200:
            return item.json()
        else:
            return {}

    def getManyResourceItems(self, attributes=None, filters=None, geo=None):
        """ Items matching the criterion
        Args:
            attributes (Dict): Array of key value pairs
                                     For e.x,
                                     {"tags": ["a", "b"], "provider": ["c"]}
            filters (List[str]): Array of strings as filter opts
                                     For e.x,
                                     ["id", "provider"]
        Returns:
            list (List[Dict]): List  of catalogue items (dicts)
        """
        url = self.getUrl() + "/search"
        opts = self.makeOpts(attributes, filters, geo)
        url = url + "?" + opts
        items = requests.get(url)
        if items.status_code is 200:
            return items.json()
        else:
            return []
