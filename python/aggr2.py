#! /usr/bin/env python3.7
from netapp_ontap import config
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
conn1 = HostConnection("192.168.0.101", username = "admin", password = "Netapp1!", verify = False)
conn2 = HostConnection("192.168.0.102", username = "admin", password = "Netapp1!", verify = False)

config.CONNECTION = conn1
aggr = Aggregate()
aggr.get()
print("Aggregates for cluster1:")
print(aggr)

config.CONNECTION = conn2
aggr = Aggregate()
aggr.get()
print("Aggregates for cluster2:")
print(aggr)
