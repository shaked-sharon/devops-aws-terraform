# DevOps AWS — Terraform Mini Project

This repo is a small, focused Terraform setup that creates:
- a **Security Group** (inbound **SSH 22** + **app 5001**, egress anywhere),
- one **EC2** instance (**t3.micro**, **Ubuntu 22.04**, **20 GB gp3** root volume),
- and (optionally) stores **remote Terraform state** in **S3**.

**Region:** `us-east-2`  
**Default tags:** `env=devops`, `owner=Sharon`

>SECURITY NOTE: opening ports **22** and **5001** to `0.0.0.0/0` is OK for class/demo NOT for production.

---

## Folder Layout

    terraform/
      aws/
        dev/                  # Environment: backend + provider + root module
          providers.tf
          main.tf
          data.tf
        modules/              # Reusable modules
          security_group/
            main.tf
            variables.tf
            outputs.tf
          ec2/
            main.tf
            variables.tf
            outputs.tf
            data.tf
    logs/
      .gitkeep                # Keeps the folder in git; real runs write provisioning.log
    .gitignore
    README.md
    requirements.txt          # (not used by Terraform; kept for consistency)

---

## Prerequisites

1) **Terraform** installed (Mac: Homebrew, Windows: Chocolatey, Linux: apt).  
2) **AWS CLI** configured with credentials and default region **us-east-2**.  
   - You can export env vars per terminal session:

        export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
        export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
        export AWS_DEFAULT_REGION="us-east-2"

3) **S3 bucket for remote state** (only if you want _remote_ backend):
   - Bucket name used here: **shaked-s3-devops** (you can change it in `providers.tf`).
   - If the bucket doesn’t exist, create and enable versioning:

        aws s3 mb s3://shaked-s3-devops --region us-east-2
        aws s3api put-bucket-versioning --bucket shaked-s3-devops --versioning-configuration Status=Enabled

4) **SSH key** at `~/.ssh/devops-key` (private) and `~/.ssh/devops-key.pub` (public).  
   - Create one if needed:

        ssh-keygen -t rsa -b 4096 -f ~/.ssh/devops-key -N ""

---

## Clean Up (avoid charges)

When you’re done, destroy the resources and log it:

    terraform destroy
    terraform destroy -auto-approve

---

## Module Documentation (terraform-docs)

Generate Registry-style docs for each module. First install the tool (Mac):

    brew install terraform-docs

Then run inside each module:

    cd terraform/aws/modules/security_group
    terraform-docs markdown . > README.md

    cd ../ec2
    terraform-docs markdown . > README.md

These `README.md` files live next to the modules and describe inputs/outputs and usage.

---

## Notes & Defaults

- **Backend (providers.tf):** configured for S3 bucket `shaked-s3-devops` in `us-east-2` with a key path under your name (adjust if needed).
- **AMI:** Ubuntu 22.04 LTS is selected via data source in the EC2 module.
- **Instance type:** `t3.micro` (fits the lab; change in `terraform/aws/modules/ec2/variables.tf` if needed).
- **Root volume:** `20GB`, `gp3`, `delete_on_termination = true`.
- **VPC/Subnet:** The environment uses your **default VPC** and first subnet found in `us-east-2` (see `terraform/aws/dev/data.tf`). If your account has no default VPC, replace with data-sourced or explicit VPC/Subnet IDs.
- **Open ports:** 22 (SSH) and 5001 (app test). Edit the `allowed_cidrs` variable in the SG module to restrict access.
- **Formatting:** run `terraform fmt -recursive` before committing, to make the code look tidy.

---

## Typical Workflow

    # 0) one-time: create S3 bucket + versioning (if using remote state)
    aws s3 mb s3://shaked-s3-devops --region us-east-2
    aws s3api put-bucket-versioning --bucket shaked-s3-devops --versioning-configuration Status=Enabled

    # 1) export AWS creds (new terminal sessions)
    export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
    export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
    export AWS_DEFAULT_REGION="us-east-2"

    # 2) run from env folder 
    cd terraform/aws/dev
    terraform init
    terraform plan
    terraform apply -auto-approve
    terraform output

    # 3) (optional) SSH to the instance
    ssh -i ~/.ssh/devops-key ubuntu@$(terraform output -raw public_ip)

    # 4) destroy when done
    terraform destroy -auto-approve

