# DevOps Final Project | AWS-Terraform | Part I

## Project Overview

This is the first part of the DevOps Final Project (Part I)  
The initial project submission was changed to use a single top-level Terraform configuration format.  
It provisions & manages one **Ubuntu EC2 instance** using my **AWS account** (no S3 used this time)  
All Terraform state remains _local_ in the **terraform/** folder

**Region:** `eu-central-1` (Frankfurt)  
**Instance type:** `t3.medium`  
**Default tags:** `env=devops`, `owner=Sharon`

> **SECURITY NOTE:** Port **22** (SSH) - Currently open only to personal/home IPv4/32  
> **Port 5001**: Open to `0.0.0.0/0` **NOTE:** For testing/student project use **ONLY!!** _Never_ use this in prod!!

---

## What This Project Does

1. **Infrastructure Provisioning**
   - Creates & manages single EC2 instance using Terraform  
   - Configures AWS Security Group rules > allow SSH (22) from home IPv4/32 & TCP (5001) from 0.0.0.0/0  
   - Uses default tags: env=devops, owner=Sharon, Name=builder > Tag AWS resources  
   - Uses local Terraform state files stored > terraform folder  

2. **Configuration Management**
   - Retrieves latest Canonical Ubuntu LTS AMI (`owner = 099720109477`)  
   - Detects default VPC & public subnets (eu-central-1)  
   - Defines region, instance type, & CIDR > `terraform.tfvars`  

3. **Automation & Logs**
   - Logs Terraform commands & outputs using `log.sh` script (output in `session_log.txt`)  
   - Demonstrates Git branching workflow: feature > dev > main  

4. **Validation & Cleanup**
   - Builds EC2 instance  
   - Verifies SSH connectivity  
   - Destroy once complete to avoid AWS charges  

---

## Current Implementation

- Full Terraform setup (provider, variables, data, main, outputs, tfvars)  
- EC2 instance: Ubuntu 22.04 LTS (Canonical), t3.medium  
- Local backend (no S3)  
- 20 GB gp3 root volume  
- Security Group: port 22 open to home IPv4/32; port 5001 open to 0.0.0.0/0  
- Tags used: env=devops, owner=Sharon, Name=builder  
- Git workflow: feature > dev > main  
- SSH connectivity verified  
- Terraform destroy executed successfully  

---

## Future Components to be Added

- **Web App:** To be added in future project addition  
- **Load Balancer:** Future component for scaling project  
- **Docker, Jenkins, CI/CD Integration:** To be integrated in future part of project  
- **Kubernetes & Helm:** To be added in future for autoscaling or monitoring  

---

## Setup & Installation

### Prereqs
1. **Terraform CLI** installed  
2. **AWS IAM access keys** EC2 & VPC permissions  

Export credentials _before_ running/executing Terraform:

```
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
export AWS_DEFAULT_REGION="eu-central-1"
```

---

## How to Execute:

1. **Go to terraform folder path**
   ```
   cd terraform (or relevant path to terraform folder)
   ```
2. **Generate SSH key pair (private local key ONLY)**
   ```
   ssh-keygen -t rsa -b 4096 -m PEM -f builder_key.pem -N ""
   ```
3. **Find IPv4 & append /32**
   ```
   curl -4 ifconfig.me _(ensure IPv4 not IPv6)_
   OR
   curl -s ipv4.icanhazip.com _(if previous command returns IPv6)_
   ```
   _i.e._ IPv4 format: `xxx.xx.xx.68/32`
4. **Edit terraform.tfvars**
   ```
   region           = "eu-central-1"
   instance_type    = "t3.medium"
   key_name         = "builder-key"
   private_key_path = "./builder_key.pem"
   home_cidr = "YOUR_IPV4_ADDRESS/32"
   open_world_port  = 5001
   name_prefix      = "builder"
   ```
5. **Run Terraform**
   ```
   terraform init
   terraform plan
   terraform apply -auto-approve
   terraform output
   ```
6. **Expected Outputs**
   ```
   public_ip              = "x.x.x.x"
   security_group_id      = "sg-xxxxxxxxxxxx"
   private_key_local_path = "./builder_key.pem"
   ```
7. **SSH into Instance**
   ```
   ssh -i builder_key.pem ubuntu@<_public_ip_>
   ```
8. **Exit SSH session once verification is complete**
   ```
   exit
   ```
9. **Destroy resources when done** _(ensures no AWS charges incurred)_
   ```
   terraform destroy -auto-approve
   ```

---

## Files Explained

- **provider.tf** – AWS provider & default tags  
- **variables.tf** – region, instance_type, key, CIDRs  
- **data.tf** – AMI / default VPC / public subnets  
- **main.tf** – key pair, SG, EC2 resources  
- **outputs.tf** – prints public_ip, SG ID, local key path  
- **terraform.tfvars** – personal values > region, CIDR, key paths  
- **log.sh** – script for logging > session_log.txt  
- **session_log.txt** – command & output logfile  
- **python/builder_client.py** – placeholder for later project parts  
- **python/README.md** – marks Python folder ungraded for Part I  
- **.gitignore** – ignores keys, secrets, Terraform cache files  
- **README.md** – this file you’re currently reading :)  

---

## Education Goals

This project demonstrates:
- Terraform fundamentals & AWS provisioning  
- Infrastructure-as-Code using real cloud resources  
- Secure credential handling via environment variables  
- Git branching & pull request (PR) workflow (mimics real world execution style)  
- Logging & reproducibility using Bash scripts  
- Verification via SSH access & teardown practice  

---

## Future Additions to DevOps Final Project

**Part I | AWS - Terraform Infrastructure**  
- Foundation for a complete CI/CD pipeline  

**Part II – Docker & Containerization**  
- Build multi-stage Dockerfile for Flask AWS-monitoring app  
- Run container on EC2  

**Part III – Flask Debug & AWS Integration**  
- Flask app lists EC2, VPCs, Load Balancers, AMIs  
- Update and verify Docker image  

**Part IV – CI/CD Pipelines | Jenkins / Azure**  
- Jenkins and Azure DevOps pipelines for Docker builds  
- Secure credentials and automated stages  

**Part V – Kubernetes & Helm**  
- Package Flask app as Helm chart  
- Deploy to Kubernetes with yaml  

**Final Goal**  
Complete automated DevOps workflow that:  
- Provisions infrastructure with Terraform  
- Containerizes apps using Docker  
- Automates CI/CD with Jenkins and Azure DevOps  
- Deploys via Kubernetes and Helm  

_**This project will evolve into a full cloud-native delivery pipeline.**_

---

## Author

**Sharon Shaked (shaked-sharon)**  
- **Email:** sharon.shaked@icloud.com / sharon.shaked24@gmail.com  
- **GitHub:** https://github.com/shaked-sharon

---

## License

This project is for **educational purposes only** & is part of a **DevOps Program** final project
