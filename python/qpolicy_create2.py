#! /usr/bin/env python3.7
"""
ONTAP 9.7 REST API Python Client Library Scripts: This script performs the following:
        - Create a quota policy rule
usage: python3.7 qpolicy_create.py [-h] -c cluster -v VOLUME_NAME -vs VSERVER_NAME -q QTREE_NAME
       -sh SPACE_HARD -fh FILE_HARD -un USER_NAME [-u API_USER] [-p API_PASS]
"""

from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaRule

with HostConnection("cluster1", username="admin", password="Netapp1!", verify=False):
    resource = QuotaRule()
    resource.svm = {"name": "VServer1"}
    resource.volume = {"name": "Vol1"}
    resource.type = "user"
    resource.users = [{"name": "admin"}]
    resource.qtree = {"name": "QTree1"}
#    resource.user_mapping = "on"
    resource.space = {"hard_limit": 8192, "soft_limit": 1024}
    resource.files = {"hard_limit": 20, "soft_limit": 10}
    resource.post(hydrate=True)
    print(resource)
'''
with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QuotaRule()
    resource.svm = {"name": "svm1"}
    resource.volume = {"name": "vol1"}
    resource.type = "user"
    resource.users = [{"name": "jsmith"}]
    resource.qtree = {"name": "qt1"}
    resource.user_mapping = "on"
    resource.space = {"hard_limit": 8192, "soft_limit": 1024}
    resource.files = {"hard_limit": 20, "soft_limit": 10}
    resource.post(hydrate=True)
    print(resource)
'''