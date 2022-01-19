#! /usr/bin/env python3.7
"""
ONTAP 9.7 REST API Python Client Library Scripts: This script performs the following:
        - Create a quota policy rule
usage: python3.7 qpolicy_create.py [-h] -c cluster -v VOLUME_NAME -vs VSERVER_NAME -q QTREE_NAME
       -sh SPACE_HARD -fh FILE_HARD -un USER_NAME [-u API_USER] [-p API_PASS]
"""

import argparse
from getpass import getpass
import logging

from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import QuotaRule

def create_policy_rule(vserver_name: str, volume_name: str,  user_name: str, qtree_name: str, space_hard: int, file_hard: int) -> None:
    '''
    Using as reference for the required fields: https://library.netapp.com/ecmdocs/ECMLP2858435/html/resources/quota_rule.html
    with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
        resource = QuotaRule()
        resource.svm.name = "svm1"
        resource.volume.name = "vol1"
        resource.type = "user"
        resource.users = [{"name": "jsmith"}]
        resource.qtree.name = "qt1"
        resource.user_mapping = "on"
        resource.space.hard_limit = 8192
        resource.space.soft_limit = 1024
        resource.files.hard_limit = 20
        resource.files.soft_limit = 10
        resource.post(hydrate=True)
        print(resource)
    '''
    data = {
        'svm': {'name': vserver_name},
        'volume': {'name': volume_name},
        'type': 'user',
        # ERROR: AttributeError: 'Namespace' object has no attribute 'user_name'
        # resource.users = [{"name": "jsmith"}]
        'users': {'name': user_name},
        #ERROR SOLUTION:
        #In the  parse_args(), the highlighted should be user_name.
        #    parser.add_argument("-un", "--users_name", required=True, help="Quota Users name")
        'qtree': {'name': qtree_name},
        'user_mapping': 'on',
        'space': {'hard_limit': space_hard, 'soft_limit': 100},
        'files': {'hard_limit': file_hard, 'soft_limit': 100},
    }
    quotarule = QuotaRule(**data)
    try:
        quotarule.post()
        print("Rule 'tree' created successfully for %s" % qtree_name)
    except NetAppRestError as err:
        print("Error: Rule was not created: %s" % err)
    return

def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""
    parser = argparse.ArgumentParser(
        description="This script will create a new quota policy for a qtree."
    )
    parser.add_argument(
        "-c", "--cluster", required=True, help="API server IP:port details"
    )
    parser.add_argument(
        "-svm", "--vserver_name", required=True, help="SVM to create the volume from"
    )
    parser.add_argument(
        "-v", "--volume_name", required=True, help="Volume to create the qtree in"
    )
    parser.add_argument(
        "-q", "--qtree_name", required=True, help="Qtree name"
    )
    parser.add_argument(
        "-un", "--user_name", required=True, help="Quota Users name"
    )
    parser.add_argument(
        "-sh", "--space_hard", required=False, help="Space Hard Limit"
    )
    parser.add_argument(
        "-fh", "--file_hard", required=False, help="File Hard Limit"
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
    # Create a policy rule for the qtree
    create_policy_rule(args.volume_name, args.vserver_name, args.qtree_name, args.user_name, args.space_hard, args.file_hard)
