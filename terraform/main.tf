# Data sources: Canonical Ubuntu LTS, default VPC, subnets
data "aws_ami" "ubuntu_lts" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = [
      "ubuntu/images/hvm-ssd/ubuntu-noble-24.04-amd64-server-*",
      "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
    ]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "in_default_vpc" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# get public key from local key path (./builder_key.pub)
locals {
  public_key_path = regexreplace(var.private_key_path, "\\.pem$", ".pub")
}

# locally generated public key (.pub) for AWS key pair
resource "aws_key_pair" "builder" {
  key_name   = var.key_name
  public_key = file(local.public_key_path)
  tags = {
    Name = "builder"
  }
}

# Security Group: SSH from home /32 & port 5001 (open to world)
# egress allows all
resource "aws_security_group" "builder_sg" {
  name        = "builder-sg"
  description = "SSH from home and 5001 open to world"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "SSH from home"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.home_cidr]
  }

  ingress {
    description = "app port open to world"
    from_port   = var.open_world_port
    to_port     = var.open_world_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "all egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "builder-sg"
  }
}

# EC2 instance > default VPC
# ensure public IP
# 20GB gp3
# Name=builder
resource "aws_instance" "builder" {
  ami                         = data.aws_ami.ubuntu_lts.id
  instance_type               = var.instance_type
  subnet_id                   = element(data.aws_subnets.in_default_vpc.ids, 0)
  vpc_security_group_ids      = [aws_security_group.builder_sg.id]
  key_name                    = aws_key_pair.builder.key_name
  associate_public_ip_address = true

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  tags = {
    Name = "builder"
  }
}