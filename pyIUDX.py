import sys
import json
import urllib3
import requests

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
	def __init__(self, auth_server, certificate, key, auth_version= 1):
		self.url		= "https://" + auth_server + "/auth"+"/v"+ str(auth_version)
		self.credentials	= (certificate, key)

	def call(self,api,body = None):

		body = json.dumps(body)

		if api == "acl":
			connect = requests.get(self.url + "/" + api, cert = self.credentials, verify = True) 
		else:
			connect = requests.post(self.url + "/" + api, cert = self.credentials, verify = True, data = body, headers = {"content-type":"application/json"})

		if connect.status_code != 200:
			sys.stderr.write("Auth failure : " + str(connect.status_code) + " : " + connect.text)
			return None
		else:
			return json.loads(connect.text)

	def get_token(self, request, token_time = None, existing_token = None):

		body = {'request' : request}

		if token_time:
			body['token-time']	= token_time 
		if existing_token:
			body['existing-token']	= existing_token 

		return self.call("token",body)

	def get_policy(self):
		return self.call("acl")

	def set_policy(self,policy):
		body = {'policy' : policy}
		return self.call("acl/set",body)

	def append_policy(self,policy):
		body = {'policy' : policy}
		return self.call("acl/append",body)

	def introspect_token(self,token):
		body = {'token' : token}
		return self.call("introspect",body)

	def revoke_token (self,tokens, token_hashes = None):

		if token_hashes:

			assert (tokens == None) # either tokens or token-hashes must be provided, not both

			if type(token_hashes) == type('string'):
				body = {'token-hashes' : [token_hashes]}
			else:
				assert (type(token_hashes) == type([])) # must be a list
				body = {'token-hashes' : token_hashes }
		else:

			assert (token_hashes == None) # either tokens or token-hashes must be provided, not both

			if type(tokens) == type('string'):
				body = {'tokens' : [tokens]}
			else:
				assert (type(tokens) == type([])) # must be a list
				body = {'tokens' : tokens }

		return self.call("introspect",body)

	def audit_tokens(self,hours):
		body = {'hours': hours}
		return self.call("audit/tokens",body)

	def add_consumer_to_group (self,consumer,group):
		body = {'consumer' : consumer, 'group' : group}
		return self.call("group/add",body)

	def delete_consumer_from_group (self,consumer,group):
		body = {'consumer' : consumer, 'group' : group}
		return self.call("group/delete",body)

	def list_group (self,consumer,group = None):
		body = {'consumer' : consumer}

		if group:
			body['group'] = group

		return self.call("group/list",body)

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


