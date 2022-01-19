#! /usr/bin/env python3.7
from netapp_ontap import config
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
conn = HostConnection("192.168.0.102", username = "admin", password = "Netapp1!", verify = False)
config.CONNECTION = conn
aggr = Aggregate()
aggr.get()
print(aggr)

print("Other option:")
print(list(Aggregate.get_collection()))

print("Other option:")
for x in Aggregate.get_collection():
 x.get()
 print(x)
 print(x.name)
 print(x, type(x))
