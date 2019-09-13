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
       url = self._catDomain+":"+self._catPort+"/catalogue"+"/v"+self._catVersion+"/search"
       connect = requests.get(url, verify=False)
       return(connect.status_code)
    
    def getAllItems(self):
       url = self._catDomain+":"+self._catPort+"/catalogue"+"/v"+self._catVersion+"/search"
       items = requests.get(url, verify=False)
       return(items.json())

    def getItemCount(self):
       url = self._catDomain+":"+self._catPort+"/catalogue"+"/v"+self._catVersion+"/count"
       count = requests.get(url, verify=False)
       return(count.json())
    
    def getResourceItem(self):
	url = self._catDomain+":"+self._catPort+"/catalogue"+"/v"+self._catVersion+"/search"+"?attribute-filter="+"("+attributeFilter[0]+","+attributeFilter[1]+")"
	filteredItems = requests.get(url, verify=False)
	return(filteredItems.json())


    
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
