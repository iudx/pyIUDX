import requests


"""
    TODO: Upload items
"""


class Catalogue():
    def __init__(self, catUrl):
        """Catalogue base class constructor
        Args:
            catUrl (string): catalogue url
        """
        self._cat_url = catUrl

    def checkConnection(self):
        connect = requests.get(self._cat_url)
        if connect.status_code != 200:
            raise RuntimeError("Couldn't connect to catalogue server")

    def all(self):
        """ Get all catalogue items
        Returns:
            list (List[Dict]): List  of catalogue items (dicts)
        TODO: Paginate
        """
        url = self._cat_url + "/search"
        items = requests.get(url)
        return(items.json())

    def make_opts(self, attributes=None, filters=None, geo=None):
        """Make attributes options string
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
        attr_opts = ""
        attr_keys = []
        attr_values = []
        filter_opts = ""
        geo_opts = ""
        if attributes is not None:
            for attr in attributes.keys():
                attr_keys.append(attr)
                attr_values.append(attributes[attr])
            attr_opts = ("attribute-name=(" + ",".join(a for a in attr_keys) + ")&" +
                        "attribute-value=(" +
                        "".join(str(tuple(a)).replace("\'", "")
                                for a in attr_values) + ")")
        if filters is not None:
            filter_opts = ("attribute-filter=" +
                          str(tuple(filters)).replace("\'", ""))

        if geo is not None:
            geo_keys = list(geo.keys())
            if len(geo_keys) is not 1:
                raise RuntimeError("Multiple Geo Options not supported")
            geo_key = geo_keys[0]

            try:
                if geo_key is "circle":
                    geo_opts = ("lat=" + str(geo[geo_key]["lat"]) + "&" +
                               "lon=" + str(geo[geo_key]["lon"]) + "&" +
                               "radius=" + str(geo[geo_key]["radius"]))

                if geo_key is "polygon":
                    if geo[geo_key][0] != geo[geo_key][-1]:
                        raise RuntimeError("Last point not equal to first point")
                    geo_opts = ("geometry=polygon(" +
                               ",".join(str(g[0]) + "," + str(g[1])
                                        for g in geo[geo_key]) + ")" +
                               "&relation=within")

                if geo_key is "bbox":
                    if len(geo[geo_key]) != 2:
                        raise RuntimeError("Two points needed for bbox query")
                    geo_opts = ("bbox=" +
                               ",".join(str(g[0]) + "," + str(g[1])
                                        for g in geo[geo_key]) +
                               "&relation=within")

                if geo_key is "line":
                    geo_opts = ("geometry=linestring(" +
                               ",".join(str(g[0]) + "," + str(g[1])
                                        for g in geo[geo_key]) + ")" +
                               "&relation=intersects")

            except Exception as e:
                raise RuntimeError("Incorrect parameter given.\n", e)

        opts = (attr_opts +
                ("&" if attributes is not None else "") + filter_opts +
                ("&" if filters is not None else "") + geo_opts)
        return opts

    def count(self, attributes=None, filters=None, geo=None):
        """Number of items matching the criterion
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
        url = self._cat_url + "/count"
        opts = self.make_opts(attributes, filters, geo)
        url = url + "?" + opts
        count = requests.get(url)
        if count.status_code is 200:
            return count.json()["Count"]
        else:
            return -1


    def get_data_model(self, item_id):
        """Get the data model for a given id
        Returns:
            list (List[Dict]): List  of catalogue items (dicts)
        """
        item = self.get(item_id)
        try:
            dm = requests.get(item["refDataModel"]["value"]).json()
        except:
            raise RuntimeError("Couldn't load data model")
        return(dm)

    def get(self, item_id=None, attributes=None, filters=None, geo=None):
        """Items matching the criterion or single item if item_id is provided
        Args:
            item_id (String): ID of the item
            attributes (Dict): Array of key value pairs
                                     For e.x,
                                     {"tags": ["a", "b"], "provider": ["c"]}
            filters (List[str]): Array of strings as filter opts
                                     For e.x,
                                     ["id", "provider"]
        Returns:
            list (List[Dict]): List  of catalogue items (dicts)
        """
        if item_id is not None:
            url = self._cat_url + "/items" + "/" + item_id
            opts = self.make_opts(None, filters)
            url = url + "?" + opts
            item = requests.get(url)
            if item.status_code is 200:
                return item.json()[0]
            else:
                return {}

        url = self._cat_url + "/search"
        opts = self.make_opts(attributes, filters, geo)
        url = url + "?" + opts
        items = requests.get(url)
        if items.status_code is 200:
            return items.json()
        else:
            return []
