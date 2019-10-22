import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Catalogue():
    def __init__(self, catDomain, catPort, catVersion=1):
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
        url = (self._catDomain + ":" + self._catPort +
               "/catalogue" + "/v" + self._catVersion + "/search")
        connect = requests.get(url)
        if connect.status_code != 200:
            raise RuntimeError("Couldn't connect to catalogue server")

    def dispParams(self):
        """ Display catalogue initalization parameter
        Returns:
            (catDomain, catPort, catVersion) (string, string, string): version string
        """
        return self._catDomain, self._catPort, self._catVersion

    def get_url(self):
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
        url = self.get_url() + "/search"
        items = requests.get(url)
        return(items.json())

    def makeOpts(self, attributes=None, filters=None):
        """ Make attributes options string
        Args:
            attributes (List[Dict]): Array of key value pairs
                                     For e.x,
                                     [{attribute_name: (string),
                                       attribute_values: List(string)}]
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
        if attributes is not None:
            for attr in attributes:
                attrKeys.append(attr["attribute_name"])
                attrValues.append(attr["attribute_values"])
            attrOpts = ("attribute-name=(" + ",".join(a for a in attrKeys) + ")&" +
                        "attribute-values=(" +
                        "".join(str(tuple(a)).replace("\"", "") for a in attrValues))
        if filters is not None:
            filterOpts = "attribute-filter=" + str(tuple(filters))
        opts = attrOpts + "&" + filterOpts
        return opts

    def getItemCount(self, attributes=None, filters=None):
        """ Number of items matching the criterion
        Args:
            attributes (List[Dict]): Array of key value pairs
                                     For e.x,
                                     [{attribute_name: (string),
                                       attribute_values: List(string)}]
            filters (List[str]): Array of strings as filter opts
                                     For e.x,
                                     ["id", "provider"]
        Returns:
            count (int): number of items
        """
        url = self.get_url() + "/count"
        opts = self.makeOpts(url, attributes, filters)
        url = url + "?" + opts
        count = int(requests.get(url)["Count"])
        return count

    def getResourceItem(self, resourceId, attributes=None, filters=None):
        """ Items matching the criterion
        Args:
            attributes (List[Dict]): Array of key value pairs
                                     For e.x,
                                     [{attribute_name: (string),
                                       attribute_values: List(string)}]
            filters (List[str]): Array of strings as filter opts
                                     For e.x,
                                     ["id", "provider"]
        Returns:
            list (List[Dict]): List  of catalogue items (dicts)
        """
        url = self.get_url() + "/items" + "/" + resourceId
        opts = self.makeOpts(url, attributes, filters)
        url = url + "?" + opts
        filteredItems = requests.get(url)
        return filteredItems.json()
