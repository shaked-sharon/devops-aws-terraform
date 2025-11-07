# DevOps | Final Project | AWS — Terraform | Part I

This is the first part of the DevOps Final Project (Part I)
It has changed the initial project submission using 1 top-level Terraform config 
It provisions & manages 1 **Ubuntu EC2 instance** using my personal **AWS account** (no S3 used)  
All Terraform state remains _local_ > **terraform/** folder

**Region:** `eu-central-1` (Frankfurt)  
**Instance type:** `t3.medium`  
**Default tags:** `env=devops`, `owner=Sharon`

> **SECURITY NOTE:** Port **22** (SSH) - Currenly open only to personal/home IPv4/32 
> **Port 5001**: Open to `0.0.0.0/0` **NOTE:** For testing/student project use **ONLY!!** _Never_ use this in prod!!

---

## Folder Layout

```
terraform/
  provider.tf          # AWS provider & default tags
  variables.tf         # region, instance_type, key, CIDRs
  data.tf              # AMI / default VPC / public subnets
  main.tf              # key pair, SG, EC2 resources
  outputs.tf           # prints public_ip, SG ID, local key path
  terraform.tfvars     # personal values > region, CIDR, key paths
  log.sh               # script to log > session_log.txt
  session_log.txt      # command & output logfile
  README.md            # this file you're currently reading :)
python/
  builder_client.py    # placeholder for later project parts
  README.md
.gitignore
```
---

## Prereqs

1. **Terraform CLI** installed  
2. **AWS IAM access keys** EC2 & VPC permissions  

Export credentials _before_ running/executing Terraform:

```
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
export AWS_DEFAULT_REGION="eu-central-1"
```
---

## Workflow

```
# 1) move into terraform folder
cd terraform

# 2) generate SSH key pair (private key local ONLY)
ssh-keygen -t rsa -b 4096 -m PEM -f builder_key.pem -N ""

# 3) find IPv4 & append /32
curl -4 ifconfig.me
# example result: 104.28.60.68/32

# 4) edit terraform.tfvars
region           = "eu-central-1"
instance_type    = "t3.medium"
key_name         = "builder-key"
private_key_path = "./builder_key.pem"
home_cidr        = "104.28.60.68/32"
open_world_port  = 5001
name_prefix      = "builder"

# 5) run Terraform
terraform init
terraform plan
terraform apply -auto-approve
terraform output

# 6) expected outputs
public_ip              = "x.x.x.x"
security_group_id      = "sg-xxxxxxxxxxxx"
private_key_local_path = "./builder_key.pem"

# 6) SSH into instance
ssh -i builder_key.pem ubuntu@<_public_ip_>

# 7) exit SSH session after verification complete
exit

# 8) destroy resources when done so no aws charges incurred
terraform destroy -auto-approve
```

---

## Notes / Defaults

- **AMI:** Latest Canonical Ubuntu LTS (`owner = 099720109477`)  
- **Root block device:** 20 GB, gp3  
- **Networking:** Default VPC, public subnet > eu-central-1  
- **Backend:** Local state (`terraform.tfstate` under `terraform/`)  
- **Tags:** default_tags: env = devops, owner = Sharon / Name = builder  
- **Pull Requests:** feature > dev > main branches  

---

## Submission for Part I

GitHub repo link:  
`https://github.com/shaked-sharon/devops-aws-terraform`

Main branch includes:  
- top-level Terraform configuration  
- complete session logs  
- PR merges recorded  
- EC2 instance verified and destroyed successfully  

---

### Future Additions to DevOps Final Project

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
- Deploy to Kubernetes using values.yaml  

**Final Goal**  
A complete automated DevOps workflow that:  
- Provisions infrastructure with Terraform  
- Containerizes apps using Docker  
- Automates CI/CD with Jenkins and Azure DevOps  
- Deploys via Kubernetes and Helm  

_**This project will evolve into a full cloud-native delivery pipeline.**_
