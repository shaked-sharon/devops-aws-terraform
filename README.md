# DevOps | Final Exam | AWS — Terraform Configuration

## Project Overview

DevOps Final Project — provisions AWS infrastructure using Terraform, containerizes a Python app with Docker, and automates the build/push workflow using Jenkins CI/CD pipeline running on EC2  
All Terraform state remains _local_ in **terraform/** folder

**Region:** `eu-central-1` (Frankfurt)  
**Instance type:** `t3.medium`  
**Default tags:** `env=devops`, `owner=Sharon`

> **SECURITY NOTE:** Port **22** (SSH) - Currently open only to personal/home IPv4/32  
> **Port 5001**: Open to `0.0.0.0/0` **NOTE:** For testing/student project use **ONLY!!** _Never_ use this in prod!!  
> **Port 8080**: Jenkins UI — open to `0.0.0.0/0` **NOTE:** For testing/student project use **ONLY!!** _Never_ use this in prod!!

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

5. **Docker Containerization**
   - Packages Python app (`builder_client.py`) into a Docker image  
   - Uses `python:3.11-slim` base image  
   - Image pushed to Docker Hub: `sharonshaked/builder`  

6. **Jenkins CI/CD Pipeline**
   - Jenkins runs on EC2 via Docker Compose (using instructor workshop setup)  
   - Pipeline stages: Clone > Build > Run > Push  
   - Jenkinsfile reads from GitHub repo (`feature/docker` branch)  
   - Docker Hub credentials stored securely in Jenkins credentials manager  

---

## Current Implementation

- Full Terraform setup (provider, variables, data, main, outputs, tfvars)  
- EC2 instance: Ubuntu 22.04 LTS (Canonical), t3.medium  
- Local backend (no S3)  
- 20 GB gp3 root volume  
- Security Group: port 22 open to home IPv4/32; port 5001 open to 0.0.0.0/0; port 8080 open to 0.0.0.0/0 for Jenkins  
- Tags used: env=devops, owner=Sharon, Name=builder  
- Git workflow: feature > dev > main  
- SSH connectivity verified  
- Dockerfile packages Python app into container  
- Docker image pushed to Docker Hub (`sharonshaked/builder`)  
- Jenkins running on EC2 via Docker Compose  
- Jenkins pipeline: Clone > Build > Run > Push — all stages pass  
- Docker Hub credentials managed via Jenkins credentials store  

---

## Setup & Installation

### Prereqs
1. **Terraform CLI** installed  
2. **AWS IAM access keys** EC2 & VPC permissions  
3. **Docker** installed on EC2 instance  
4. **Docker Hub account** with access token for Jenkins credentials  
5. **Jenkins** running on EC2 via Docker Compose (cloned from instructor workshop repo)  

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
   curl -4 ifconfig.me (ensure IPv4 not IPv6)
   OR
   curl -s ipv4.icanhazip.com (if previous command returns IPv6)
   ```
   _i.e._ **IPv4 format:** `xxx.xx.xx.68/32`
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

### Docker & Jenkins Setup (on EC2)

10. **SSH into EC2 & install Docker**
    ```
    sudo apt update
    sudo apt install -y docker.io
    sudo systemctl start docker
    ```
11. **Clone instructor Jenkins workshop repo**
    ```
    git clone -b jenkins-workshop --single-branch https://github.com/yanivomc/devopshift-welcome.git
    cd devopshift-welcome/welcome
    ```
12. **Install Docker Compose & start Jenkins**
    ```
    sudo apt install -y docker-compose
    sudo docker-compose up -d
    ```
13. **Access Jenkins UI**
    ```
    http://<EC2_PUBLIC_IP>:8080
    Login: admin / admin1234
    ```
14. **Add Docker Hub credentials in Jenkins**
    - Manage Jenkins > Credentials > Global > Add Credentials
    - Username: Docker Hub username
    - Password: Docker Hub access token
    - ID: dockerhub-creds
15. **Create pipeline job**
    - New Item > name: builder-pipeline > Pipeline
    - Definition: Pipeline script from SCM
    - SCM: Git
    - Repository URL: your GitHub repo URL
    - Branch: */feature/docker
    - Script Path: Jenkinsfile
16. **Run pipeline**
    - Click Build Now > verify all stages pass (Clone > Build > Run > Push)

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
- **logs/git-history.log** – saved git branch history for project defense  
- **python/builder_client.py** – Python app that prints app name & port (packaged by Docker)  
- **python/README.md** – marks Python folder ungraded for Part I  
- **Dockerfile** – recipe to package builder_client.py into a Docker container  
- **Jenkinsfile** – CI/CD pipeline: Clone > Build > Run > Push to Docker Hub  
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
- Docker containerization of a Python application  
- CI/CD pipeline automation using Jenkins  
- Pushing Docker images to Docker Hub via Jenkins pipeline  
- Running Jenkins as a Docker container on EC2  

---

## Project Sections Completed

**Section 1 | Git Setup**  
- Repository structure, branching workflow (feature > dev > main), tagged releases  

**Section 2 | AWS - Terraform Infrastructure**  
- EC2 provisioning, security groups, SSH key pair, default VPC  

**Section 3 | Docker Containerization**  
- Dockerfile packages Python app into `python:3.11-slim` container  
- Image built & tested locally and via Jenkins  

**Section 5 | Jenkins CI/CD Pipeline**  
- Jenkins runs on EC2 via Docker Compose (workshop setup from instructor repo)  
- Pipeline stages: Clone > Build > Run > Push  
- Docker image pushed to Docker Hub: `sharonshaked/builder`  
- Docker Hub credentials stored securely in Jenkins credentials manager  

**Section 5.1 | Azure DevOps** — Excluded per instructor  

## Future Additions

**Kubernetes & Helm**  
- Deploy containerized app to Kubernetes cluster  
- Package as Helm chart for repeatable deployments  

---

## Author

**Sharon Shaked (shaked-sharon)**  
- **Email:** sharon.shaked@icloud.com / sharon.shaked24@gmail.com  
- **GitHub:** https://github.com/shaked-sharon

---

## License

This project is for **educational purposes only** & is part of a **DevOps Program** final project
