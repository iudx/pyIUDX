import requests
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Catalogue():
    def __init__(self):
       self._catDomain=None
       self._catPort=None
       self._catVersion=None
    
    def dispParams(self):
       print(self._catDomain)
       print(self._catPort)
       print(self._catVersion)
    
    def connectToCat(self, catDomain, catPort, catVersion):
       self._catDomain=catDomain
       self._catPort=catPort
       self._catVersion=catVersion
       #url = self._catDomain+":"+self._catPort+"/catalogue"+"/v"+self._catVersion+"/search"
       url = self._catDomain+":"+self._catPort+"/catalogue"+"/v"+self._catVersion+"/search"
       connect = requests.get(url, verify=False)
       return(connect.status_code)
    
    def get_url(self):
        return self._catDomain + ":" + self._catPort + "/catalogue" + "/v" + self._catVersion

    def getAllItems(self):
       url = self.get_url() + "/search"
       items = requests.get(url, verify=False)
       return(items.json())

    def getItemCount(self):
       url = self.get_url() + "/count"
       count = requests.get(url, verify=False)
       return(count.json())
    
    def getResourceItem(self, resourceId):
        url = self.get_url() + "/items" + "/" + resourceId
        filteredItems = requests.get(url, verify=False)
        return(filteredItems.json())

    def getResourceItemsFor(self, attribute_name, attribute_value):
        url = self.get_url() + "/search?attribute-name=(" + attribute_name + ")&attribute-value=(" + attribute_value + ")"
        filteredItems = requests.get(url, verify=False)
        return(filteredItems.json())
    
    def getItemsofTag(self, tag):
        url = self.get_url() + "/search?attribute-name=(tags)&attribute-value=("+tag+")"
        filteredItems = requests.get(url, verify=False)
        return(filteredItems.json())
	 
    def getAllTags(self):
        self.print_dev_msg();

    def print_dev_msg(self):
        print("Yet To be developed")

class Auth():
    def __init__(self):
       self._authDomain = None 
       self._authPort = None
       self._authVersion = None
    
    def dispParams(self):
       print(self._authDomain)
       print(self._authPort)
       print(self._authVersion)
    
    def connectToAuth(self, authDomain, authPort, authVersion):
       self._authDomain = authDomain 
       self._authPort = authPort 
       self._authVersion = authVersion
       url = self._authDomain+":"+self._authPort+"/auth"+"/v"+self._authVersion
       connect = requests.get(url, verify=False)
       return(connect.status_code)


class resourceServer():
    def __init__(self):
       self._serverDomain = None 
       self._serverPort = None
       self._serverVersion = None
    
    def dispParams(self):
       print(self._serverDomain)
       print(self._serverPort)
       print(self._serverVersion)
    
    def getLatestData(self, serverDomain, serverPort, serverVersion, resource):
       self._serverDomain = serverDomain 
       self._serverPort = serverPort 
       self._serverVersion = serverVersion
       self._resource = resource
       url = self._serverDomain+":"+self._serverPort+"/api/"+self._serverVersion+"/resource/latest/"+self._resource
       latest = requests.get(url, verify=False)
       return(latest.json())


