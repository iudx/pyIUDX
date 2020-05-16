from multiprocessing import Pool, Manager
from collections import MutableSequence
from pyIUDX.rs import rs
from pyIUDX.rs import Item 
from pyIUDX.cat import cat
from pyIUDX.auth import auth
import numpy as np
import datetime
import requests
import copy

class Data:

	def __init__(self, items, properties):
		self.items = [] 
		for i in items:
			split = i.split("/") # domain / sha1 / resource-server / group / item name
			group = split[3]
			rs = "https://" + split[2] + "/resource-server/" + group + "/v1"
			catalog = "https://catalogue.iudx.org.in/catalogue/v1";
			Id = split[3:].join("/") 
			self.items.append(Item(catalog,rs,Id))

	def latest(self):
		result = []
		for i in self.items:	
			result.append(i.latest())
		return result 

	def during(self, start, end):
		result = []
		for i in self.items:	
			result.append(i.during(start,end))
		return result 

	def latestWith(self, attr, val):
		result = []
		for i in self.items:	
			result.append(i.latestWith(attr,val))
		return result 

	def valueBetween(self, attrName, minval, maxVal):
		result = []
		for i in self.items:	
			result.append(i.valueBetween(attrName,minval,maxVal))

		return result 
