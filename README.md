# DevOps | Final Exam | AWS — Terraform Configuration

This is the first part of the DevOps Final (Part I). It was changed from the earlier mini-project to a single top-level Terraform configuration.  
It provisions & manages 1 **Ubuntu EC2 instance** in my **personal AWS account** (no S3 backend).  
All Terraform state remains **local** inside `terraform/` folder.

**Region:** `eu-central-1` (Frankfurt)  
**Instance type:** `t3.medium`  
**Default tags:** `env=devops`, `owner=Sharon`

> SECURITY NOTE: Port **22** (SSH) is open only to current home IPv4/32.  
> Port **5001** is open to `0.0.0.0/0` for testing ONLY!! Do not use in prod

---

## Folder Layout

```
terraform/
  provider.tf          # AWS provider & default tags
  variables.tf         # region, instance_type, key, CIDRs, etc
  data.tf              # AMI / default VPC / public subnets
  main.tf              # key pair, SG, EC2 resources
  outputs.tf           # prints public_ip, SG ID, local key path
  terraform.tfvars     # personal values (region, CIDR, key paths)
  log.sh               # logfile to reflect in file: session_log.txt
  session_log.txt      # execution of command/output log
  README.md            # about file (you're currently reading it)
python/
  builder_client.py    # placeholder from previous module to be updated in later parts of rolling project
  README.md
.github/
  pull_request_template.md
.gitignore
PROJECT_PROMPT.md
```

---

## Prerequisites

1. **Terraform CLI** installed.  
2. **AWS IAM access keys** with EC2 + VPC read permissions.  
3. **macOS Terminal (zsh)** or any Unix-style shell.  
4. No AWS CLI required; credentials are exported manually each session.

Export environment variables before running Terraform:

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

# 3) find IPv4 & append to add /32 at end of ipv4
curl -4 ifconfig.me
# example of ipv4 with appended /32: 104.28.60.68/32

# 4) edit of terraform.tfvars
region           = "eu-central-1"
instance_type    = "t3.medium"
key_name         = "builder-key"
private_key_path = "./builder_key.pem"
home_cidr        = "104.28.60.68/32"
open_world_port  = 5001
name_prefix      = "builder"

# 5) run Terraform
./log.sh "terraform init"
./log.sh "terraform plan -out plan.out"
./log.sh "terraform apply -auto-approve plan.out"
./log.sh "terraform output"

# expected outputs
public_ip              = "x.x.x.x"
security_group_id      = "sg-xxxxxxxxxxxx"
private_key_local_path = "./builder_key.pem"

# 6) SSH into instance
ssh -i builder_key.pem ubuntu@<public_ip>

# 7) exit SSH session when verified
exit

# 8) destroy resources when finished
./log.sh "terraform destroy -auto-approve"
```

---

## Notes & Defaults

- **AMI:** Latest Canonical Ubuntu LTS (`owner = 099720109477`), most_recent = true.  
- **Root block device:** 20 GB, gp3.  
- **Networking:** Default VPC, first public subnet in eu-central-1 discovered automatically.  
- **Backend:** Local state only (`terraform.tfstate` under `terraform/`).  
- **Tags:** Applied via provider default_tags (env = devops, owner = Sharon) & Name = builder.  
- **Pull Requests:** feature > dev > main workflow recorded in session log

---

## Clean-Up and Verification

- Verify destroy success:
  ```
  ./log.sh "terraform output"
  ```
  Expected → “No outputs found.”

- Confirm in AWS Console (region = Frankfurt):  
  EC2 → Instances → none should remain.

- Commit and push final `session_log.txt`:
  ```
  ./log.sh "git add terraform/session_log.txt"
  ./log.sh "git commit -m 'final destroy logged'"
  ./log.sh "git push"
  ```

---

## Submission

Submission of GitHub repo link:  
`https://github.com/shaked-sharon/devops-aws-terraform`

Main branch includes:
- full top-level Terraform configuration,
- complete session logs,
- PR merges recorded,
- EC2 verified and destroyed successfully.