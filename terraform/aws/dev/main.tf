# Dev env integrations - modules + keypair

# Uses data.tf

# SG module
module "security_group" {
  source        = "../modules/security_group" # <-- correct relative path
  vpc_id        = data.aws_vpc.default.id
  name_prefix   = "devops-sg"
  description   = "Allow SSH (22) & app (5001)"
  allowed_cidrs = var.allowed_cidrs
}

# Key pair
resource "aws_key_pair" "this" {
  key_name   = var.key_name
  public_key = file(pathexpand(var.public_key_path))
}

# EC2 module
module "ec2" {
  source             = "../modules/ec2"
  name               = var.instance_name
  instance_type      = var.instance_type
  subnet_id          = local.selected_subnet_id
  security_group_ids = [module.security_group.security_group_id]
  key_name           = aws_key_pair.this.key_name
  user_data          = var.user_data
}