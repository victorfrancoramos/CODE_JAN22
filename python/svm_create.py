#! /usr/bin/env python3

"""
ONTAP 9.7 REST API Python Client Library Scripts: This script performs the following:
        Create sn SVM by using the netapp_ontap library.
Usage: svm_create.py [-h] -c CLUSTER -a AGGR_NAME, -vs VSERVER_NAME, [-u API_USER] [-p API_PASS]
python3.7 svm_create.py: -c cluster -a aggr_name, -vs/--vserver_name
"""

import argparse
from getpass import getpass
import logging

from netapp_ontap import config, utils, HostConnection, NetAppRestError
from netapp_ontap.resources import Svm


def create_svm(vserver_name: str, aggr_name: str) -> None:
    """Create an SVM on the specified aggregate"""

    data = {
        'name': vserver_name,
        'aggregates': [{'name': aggr_name}],
        'nfsv3': {'enabled': "true"},
        'nfsv4': {'enabled': "false"},
        'nfsv41': {'enabled': "false"}
    }

    svm = Svm(**data)

    try:
        svm.post()
        print("SVM %s created successfully" % svm.name)
    except NetAppRestError as err:
        print("Error: SVM was not created: %s" % err)
        print(err)
        print(NetAppRestError)
        print("Error code: %s" % type(err))
#        for error in NetAppRestError.get_collection():
#            pprint.pprint(error.to_dict())
#        tmp = dict(NetAppRestError.json())
#        print("Error status_code: %s " % tmp['status_code'])
#        print("Error status_code: %s" % err.status_code)
    return

def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""

    parser = argparse.ArgumentParser(
        description="This script will create a new NFS Share for a given VServer"
    )
    parser.add_argument(
        "-c", "--cluster", required=True, help="Cluster Name"
    )
    parser.add_argument(
        "-a", "--aggr_name", required=True, help="Aggregate name"
    )
    parser.add_argument(
        "-vs", "--vserver_name", required=True, help="VServer name to create NFS Share"
    )
    parser.add_argument("-u", "--api_user", default="admin", help="API Username")
    parser.add_argument("-p", "--api_pass", help="API Password")
    parsed_args = parser.parse_args()

    # collect the password without echo if not already provided
    if not parsed_args.api_pass:
        parsed_args.api_pass = getpass()

    return parsed_args


if __name__ == "__main__":
    logging.basicConfig(
        #    level=logging.DEBUG,
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)5s] [%(module)s:%(lineno)s] %(message)s",
    )

    # utils.LOG_ALL_API_CALLS = 1

    args = parse_args()
    config.CONNECTION = HostConnection(
        args.cluster, username=args.api_user, password=args.api_pass, verify=False,
    )

    create_svm(args.vserver_name, args.aggr_name)
