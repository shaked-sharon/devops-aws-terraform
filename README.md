# DevOps Automation — AWS Module

This module extends my previous project  
➡️ [DevOps Automation (Local VM Simulation)](https://github.com/shaked-sharon/devops-automation.git)  
by replacing the simulated local machines with a **real AWS EC2 instance** using **Terraform**,  
and adding a **Python script** that lists live EC2 instances with their details.

---

## What this does
- Builds a **t3.medium** EC2 instance with:
  - A **public IP**
  - A **key pair**
  - A **security group** allowing inbound TCP **22 (SSH)** and **5001 (App)**, and outbound **anywhere**
- Prints the **public IP** after `terraform apply`
- Lists EC2 instances in a formatted table (`AWS/python/list_ec2.py`)
  - Columns: **InstanceId**, **Name**, **Type**, **State**, **PublicIP**, **SecurityGroups**
- Uses **environment variables** for AWS authentication (no secrets in code)
- Integrates everything inside a friendly Python app (`cloud_manager.py`)  
  that offers both **Local** and **AWS** options.

---

## Quick Start Guide
1. Set AWS credentials in the terminal:
   ```bash
   export AWS_ACCESS_KEY_ID="YOUR_KEY"
   export AWS_SECRET_ACCESS_KEY="YOUR_SECRET"
   export AWS_DEFAULT_REGION="eu-central-1"
   ```
2. Build EC2 instance:
   ```bash
   cd AWS/terraform
   terraform init
   terraform apply -auto-approve
   ```
3. Note: **public IP** printed at the end:
   ```bash
   terraform output public_ip
   ```
4. Connect to your instance (Ubuntu AMI user):
   ```bash
   chmod 600 ~/.ssh/devops-key
   ssh -i ~/.ssh/devops-key ubuntu@<PUBLIC_IP>
   ```
5. Run Python EC2 List:
   - NOTE: If `.venv` doesn’t exist yet, create it first:
   > ```bash
   > python3 -m venv .venv
   > source .venv/bin/activate
   > pip install -r requirements.txt
   > ```
   > Then run the script:
   > ```bash
   > source .venv/bin/activate
   > python AWS/python/list_ec2.py
   
   - Then move to the following steps:
   ```bash
   source .venv/bin/activate
   python AWS/python/list_ec2.py
   ```
6. Use app menu (to view input/output menu--optional):
   ```bash
   python cloud_manager.py
   ```
   - **1)** Add local machine (simple record)
   - **2)** List local machines
   - **3)** AWS: List EC2 instances (real AWS data)
   - **4)** Exit
7. Clean up resources (avoid unneccessary charges):
   ```bash
   cd AWS/terraform
   terraform destroy -auto-approve
   ```

---

## Repo layout
```
AWS/
 ├── terraform/           # Terraform configuration files (EC2, key pair, security group)
 └── python/list_ec2.py   # Python script using boto3 + tabulate
cloud_manager.py          # Main menu: Local + AWS integration
configs/instances.json    # Local records (auto-created)
logs/app.log              # Log file (auto-created)
requirements.txt          # Python dependencies
```

---

## Project Notes
- This AWS module continues my earlier **local VM simulator** project (https://github.com/shaked-sharon/devops-automation.git)
  The local mode (created in first project) remains available inside `cloud_manager.py` to demonstrate input validation  
  & configuration -- actual infrastructure is deployed on AWS via Terraform
- The EC2 **OS** is fixed to **Ubuntu** (Terraform AMI).  
- The **SSH port** is fixed to **22**, and **TCP 5001** is open for testing future app.
- **Backups** default to enabled in local records for simplicity.  
- The `SecurityGroups` column in the EC2 list displays inbound TCP ports for each instance
- Terraform’s `public_ip` output matches the same value shown in the EC2 listing table
- SSH (22) and TCP 5001 are open to 0.0.0.0/0 for grading purposes only.
      - In production, restrict these to specific CIDR ranges or a bastion host.
- Assumes a default VPC exists in region `eu-central-1`
      - If your account has no default VPC, create one / update Terraform to use specific subnet ID

---

## Safety
- No AWS credentials or secrets are stored in code or Git history.
- `.gitignore` excludes Terraform state files, private keys, and virtual environments.
- Always run `terraform destroy` when finished to avoid charges.

---

## Author & Context
Created as part of my DevOps studies (AWS Infrastructure Module)  
and a continuation of my original **DevOps Automation** project.  
This AWS version demonstrates real infrastructure provisioning,  
automation with Terraform, and cloud resource integration via Python.

---

✅ **Final Submission:**  
GitHub Repository — [DevOps Automation — AWS Module](https://github.com/shaked-sharon/devops-automation-aws)
