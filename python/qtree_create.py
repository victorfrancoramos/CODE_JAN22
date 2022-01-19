#! /usr/bin/env python3.7

"""
ONTAP 9.7 REST API Python Client Library Scripts
Author: Victor Franco
This script performs the following:
        - Create a qtree (or a quota tree)

usage: python3.7 qtree_create.py [-h] -c CLUSTER -v VOLUME_NAME -svm SVM_NAME -q QTREE_NAME
                 [-u API_USER] [-p API_PASS]
The following arguments are required: -c/--cluster, -v/--volume_name, -svm/--svm_name, -q/--qtree_name
"""

import argparse
from getpass import getpass
import logging
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Qtree

def make_qtree(svm_name: str, volume_name: str, qtree_name: str) -> None:
    """Creates a new qtree in a volume in a SVM"""

    data = {
        'name': qtree_name,
        'svm': {'name': svm_name},
        'volume': {'name': volume_name}
    }

    qtree = Qtree(**data)

    try:
        qtree.post()
        print("Qtree %s created successfully" % qtree.name)
    except NetAppRestError as err:
        print("Error: Qtree was not created: %s" % err)
    return

def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""

    parser = argparse.ArgumentParser(
        description="This script will create a new qtree."
    )
    parser.add_argument(
        "-c", "--cluster", required=True, help="API server IP:port details"
    )
    parser.add_argument(
        "-v", "--volume_name", required=True, help="Volume to create the qtree in"
    )
    parser.add_argument(
        "-svm", "--svm_name", required=True, help="SVM to create the volume from"
    )
    parser.add_argument(
        "-q", "--qtree_name", required=True, help="Qtree name"
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
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)5s] [%(module)s:%(lineno)s] %(message)s",
    )
    args = parse_args()
    config.CONNECTION = HostConnection(
        args.cluster, username=args.api_user, password=args.api_pass, verify=False,
    )

    # Create a Qtree
    make_qtree(args.svm_name, args.volume_name, args.qtree_name)

