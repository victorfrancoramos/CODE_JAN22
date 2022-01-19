#! /usr/bin/env python3.7
"""
ONTAP 9.7 REST API Python Client Library Scripts: This script performs the following:
        - Create a qtree (or quota tree)
        - Create a quota policy rule
        - Create a QoS (Quality of Service) policy on an existing SVM
usage: python3.7 qtree.py [-h] -c cluster -v VOLUME_NAME -vs VSERVER_NAME -q QTREE_NAME
       -qos QOS_POLICY_NAME -sh SPACE_HARD -fh FILE_HARD -un USER_NAME [-u API_USER] [-p API_PASS]
"""

import argparse
from getpass import getpass
import logging

from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Qtree, QuotaRule, QosPolicy

def create_qtree(volume_name: str, vserver_name: str, qtree_name: str) -> None:
    data = {
        'name': qtree_name,
        'volume': {'name': volume_name},
        'svm': {'name': vserver_name},
        'security_style': 'unix',
        'unix_permissions': 744,
        'export_policy_name': 'default',
        'qos_policy': {'max_throughput_ops': 1000}
    }
    qtree = Qtree(**data)
    try:
        qtree.post()
        print("Qtree %s created successfully" % qtree.name)
    except NetAppRestError as err:
        print("Error: QTree was not created: %s" % err)
    return

def create_policy_rule(volume_name: str, vserver_name: str, qtree_name: str, user_name: str,
space_hard: int, file_hard: int) -> None:
    data = {
        'qtree': {'name': qtree_name},
        'volume': {'name': volume_name},
        'svm': {'name': vserver_name},
        'files': {'hard_limit': file_hard, 'soft_limit': 100},
        'space': {'hard_limit': space_hard, 'soft_limit': 100},
        'type': 'user'
    }
    quotarule = QuotaRule(**data)
    try:
        quotarule.post()
        print("Rule 'tree' created successfully for %s" % qtree_name)
    except NetAppRestError as err:
        print("Error: Rule was not created: %s" % err)
    return

def create_qos_policy(vserver_name: str, qos_policy_name: str) -> None:
    data = {
        'name': qos_policy_name,
        'svm': {'name': vserver_name},
        'adaptive': {'expected_iops': 5000, 'peak_iops': 6000, 'absolute_min_iops': 1000}
    }
    qospolicy = QosPolicy(**data)
    try:
        qospolicy.post()
        print("QoS Policy %s created successfully" % qos_policy_name)
    except NetAppRestError as err:
        print("Error: Policy was not created: %s" % err)
    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)5s] [%(module)s:%(lineno)s]
                        %(message)s")
    args = parse_args()
    config.CONNECTION = HostConnection(args.cluster, username=args.api_user, password=args.api_pass,
                                       verify=False)
    # Create a quota tree and a policy rule for the qtree
    create_qtree(args.volume_name, args.vserver_name, args.qtree_name)
    create_policy_rule(args.volume_name, args.vserver_name, args.qtree_name,
                            args.user_name,args.space_hard, args.file_hard)
    create_qos_policy(args.vserver_name, args.qos_policy_name)
