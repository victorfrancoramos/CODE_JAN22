#! /usr/bin/env python3.7

"""
ONTAP 9.7 REST API Python Client Library Scripts
Author: Victor Franco
This script performs the following:
        - Create a qtree (or a quota tree)
        - Create a quota policy rule
        - Create a QoS policy on an existing SVM

usage: python3.7 qtree.py [-h] -c CLUSTER -v VOLUME_NAME -svm SVM_NAME -q QTREE_NAME -qos QOS_POLICY_NAME
               -sh SPACE_HARD_LIMIT -fh FILE_HARD_LIMIT -un USERS_NAME [-u API_USER] [-p API_PASS]
The following arguments are required: -c/--cluster, -v/--volume_name, -vs/--vserver_name,
                -q/--qtree_name, -qos/--qos_policy_name, -sh/--space_hard_limit, -fh/--file_hard_limit
                -un/--users_name
"""

import argparse
from getpass import getpass
import logging

from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Qtree, QuotaRule, QosPolicy

def make_qtree(svm_name: str, volume_name: str, qtree_name: str) -> None:
    """Creates a new qtree in a volume in a SVM"""

    data = {
        'name': qtree_name,
        'svm': {'name': svm_name},
        'volume': [{'name': volume_name}]
    }

    qtree = Qtree(**data)

    try:
        qtree.post()
        print("Qtree %s created successfully" % qtree.name)
    except NetAppRestError as err:
        print("Error: Qtree was not created: %s" % err)
    return

def make_quota_rule(svm_name: str, volume_name: str, users_name: str, space_hard_limit: str, file_hard_limit: str) -> None:
    """Creates a new Users Quota Rule. (type set to user -no choice among user, quote or qtree-)"""

    data = {
        'svm': {'name': svm_name},
        'volume': [{'name': volume_name}],
        'type': "user",
        'users_name': {'name': users_name},
        'space_hard_limit': {'name': space_hard_limit},
        'file_hard_limit': {'name': file_hard_limit}
    }

    quota_rule = QuotaRule(**data)

    try:
        quota_rule.post()
        print("Quota Rule %s created successfully" % quota_rule.name)
    except NetAppRestError as err:
        print("Error: Quota Rule was not created: %s" % err)
    return

def make_qos_policy(svm_name: str, qos_policy_name: str) -> None:
    """Creates a new QoS Policy"""

    data = {
        'name': qos_policy_name,
        'svm': {'name': svm_name},
        'fixed.capacity_shared': False,
        'fixed.max_throughput_iops': 10000,
        'fixed.min_throughput_iops': 5000
    }

    qos_policy = QosPolicy(**data)

    try:
        qos_policy.post()
        print("QoS Policy %s created successfully" % qtree.name)
    except NetAppRestError as err:
        print("Error: QoS Policy was not created: %s" % err)
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
    parser.add_argument(
        "-qos", "--qos_policy_name", required=True, help="QoS policy name"
    )
    parser.add_argument(
        "-sh", "--space_hard_limit", required=False, help="Space Hard Limit"
    )
    parser.add_argument(
        "-fh", "--file_hard_limit", required=False, help="File Hard Limit"
    )
    parser.add_argument(
        "-un", "--users_name", required=True, help="Quota Users name"
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

    # Create a Quota Rule
    make_quota_rule(args.svm_name, args.volume_name, args.users_name, args.space_hard_limit, args.file_hard_limit)

    # Create a QoS Policy
    make_qos_policy(args.svm_name, args.qos_policy_name)
