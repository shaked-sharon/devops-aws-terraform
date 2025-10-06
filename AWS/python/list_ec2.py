#!/usr/bin/env python3
# EC2 table list
# Uses env vars > auth only

import os
import sys
import boto3
from tabulate import tabulate
from botocore.exceptions import BotoCoreError, ClientError

def get_inbound_tcp_ports(ec2, group_ids):
    """Return sorted list of TCP ports for given SG ID #'s"""
    if not group_ids:
        return []
    try:
        resp = ec2.describe_security_groups(GroupIds=group_ids)
    except (BotoCoreError, ClientError) as e:
        # Display empty ports
        print(f"Boo! Error reading security groups: {e}")
        return []
    ports = set()
    for sg in resp.get("SecurityGroups", []):
        for perm in sg.get("IpPermissions", []):
            if perm.get("IpProtocol") != "tcp":
                continue
            # single port (From > To)
            if "FromPort" in perm and "ToPort" in perm:
                fp = perm["FromPort"]
                tp = perm["ToPort"]
                if isinstance(fp, int) and isinstance(tp, int):
                    if fp == tp:
                        ports.add(fp)
                    else:
                        # Range adds both ends
                        ports.add(fp)
                        ports.add(tp)
    return sorted(ports)

def main():
    # default region > Frankfurt unless manually changed
    region = os.getenv("AWS_DEFAULT_REGION", "eu-central-1")

    # sanity check > ensure env vars exist
    missing = [k for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION") if not os.getenv(k)]
    if missing:
        print("Boo! Error! Missing AWS env vars. Please export:")
        print('  export AWS_ACCESS_KEY_ID="..."')
        print('  export AWS_SECRET_ACCESS_KEY="..."')
        print('  export AWS_DEFAULT_REGION="eu-central-1"')
        sys.exit(1)

    try:
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.describe_instances()
    except (BotoCoreError, ClientError) as e:
        print(f"Boo! Error talking to AWS: {e}")
        sys.exit(1)

    rows = []
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            # Name tag
            name = ""
            for t in instance.get("Tags", []) or []:
                if t.get("Key") == "Name":
                    name = t.get("Value") or ""
                    break

            # security group IDs > EC2 instance
            sg_ids = [sg.get("GroupId") for sg in instance.get("SecurityGroups", []) if sg.get("GroupId")]
            inbound_ports = get_inbound_tcp_ports(ec2, sg_ids)
            ports_text = ",".join(str(p) for p in inbound_ports) if inbound_ports else ""

            rows.append([
                instance.get("InstanceId", ""),
                name,
                instance.get("InstanceType", ""),
                (instance.get("State") or {}).get("Name", ""),
                instance.get("PublicIpAddress", ""),  # Terraform Public IP output
                ports_text
            ])

    if not rows:
        print(f"Boo!! Error! No EC2 instances found in region {region}")
        return

    print(tabulate(
        rows,
        headers=["InstanceId", "Name", "Type", "State", "PublicIP", "SecurityGroups"],
        tablefmt="github"
    ))
    print("\nSuccess!! EC2 instance listed. Hooray!!\n")

if __name__ == "__main__":
    main()