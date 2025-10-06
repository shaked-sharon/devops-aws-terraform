#!/usr/bin/env python3
# EC2 lister table
# Use of env vars only for auth

import os
import sys
import boto3
from tabulate import tabulate
from botocore.exceptions import BotoCoreError, ClientError

def main():
    # defaults to Frankfurt region (unless region is manually changed)
    region = os.getenv("AWS_DEFAULT_REGION", "eu-central-1")

    # sanity check: ensures env vars exist (double check)
    missing = [k for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION") if not os.getenv(k)]
    if missing:
        print("Boo! Error! Missing AWS env vars. Please export:")
        print('  export AWS_ACCESS_KEY_ID="..."')
        print('  export AWS_SECRET_ACCESS_KEY="..."')
        print('  export AWS_DEFAULT_REGION="eu-central-1"')
        sys.exit(1)

    # talk > AWS
    try:
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.describe_instances()
    except (BotoCoreError, ClientError) as e:
        print(f"Boo! Error talking to AWS: {e}")
        sys.exit(1)

    # collect rows > table
    rows = []
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            # find name tag -- if exists
            name = ""
            for t in instance.get("Tags", []) or []:
                if t.get("Key") == "Name":
                    name = t.get("Value") or ""
                    break
            rows.append([
                instance.get("InstanceId", ""),
                name,
                instance.get("InstanceType", ""),
                (instance.get("State") or {}).get("Name", ""),
                instance.get("PublicIpAddress", "")
            ])

    if not rows:
        print(f"No EC2 instances found in region {region}. Boo! I'm sad...")
        return

    # print the nice table
    print(tabulate(rows, headers=["InstanceId", "Name", "Type", "State", "PublicIP"], tablefmt="github"))
    print("Listed EC2 instances. Hooray! Success!!")

if __name__ == "__main__":
    main()