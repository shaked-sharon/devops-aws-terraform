# DevOps Automation — AWS Module

This module replaces the local VM simulation with a real EC2 instance using Terraform and adds a Python script that lists EC2 instances.

## What this does
- Builds a **t3.medium** EC2 with a **public IP**, **key pair**, and **security group** (TCP 22, 5001 in; all out).
- Prints the **public IP** after `terraform apply`.
- Provides `AWS/python/list_ec2.py` that prints a table of EC2 instances.
- Uses **environment variables** for AWS auth (no secrets in code).

## Quick start (high level)
1. Set AWS credentials in the terminal (env vars).
2. `cd AWS/terraform && terraform init && terraform apply`
3. SSH to the instance with your `.pem` key.
4. Run `AWS/python/list_ec2.py` to list instances.
5. `terraform destroy` to clean up (avoid charges).

## Repo layout
- `AWS/terraform` — Terraform for EC2
- `AWS/python` — Python script(s) using `boto3`

## Safety
- No credentials committed.
- `.gitignore` excludes Terraform state and key files.
