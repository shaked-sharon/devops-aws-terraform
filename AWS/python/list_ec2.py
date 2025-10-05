#!/usr/bin/env python3
"""
Simple EC2 script using boto3
Requirements: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION set in environment.
"""

import boto3
from tabulate import tabulate
from botocore.exceptions import BotoCoreError, ClientError
import sys
import os

def main():
    region = os.getenv("AWS_DEFAULT_REGION", "eu-central-1")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.describe_instances()
    except (BotoCoreError, ClientError) as e:
        print(f"Error connecting to AWS: {e}")
        sys.exit(1)

    instances = []
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            state = instance.get("State", {}).get("Name", "")
            public_ip = instance.get("Public-IP-Address", "")
            inst_type = instance.get("Instance-Type", "")
            instance_id = instance.get("Instance-ID", "")
            name = ""
            for tag in instance.get("Tags", []) or []:
                if tag.get("Key") == "Name":
                    name = tag.get("Value")
                    break
            instances.append([instance_id, name, inst_type, state, public_ip])

    if not instances:
        print(f"No EC2 instances found in region {region}. Boo!")
        return

    headers = ["Instance-ID", "Name", "Type", "State", "Public-IP"]
    print(tabulate(instances, headers=headers, tablefmt="github"))

if __name__ == "__main__":
    main()