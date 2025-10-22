# Lookup default VPC in current region > us-east-2
data "aws_vpc" "default" {
  default = true
}

# Get all subnets within VPC
data "aws_subnets" "default_vpc_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

locals {
  # 1st subnet id
  selected_subnet_id = data.aws_subnets.default_vpc_subnets.ids[0]
}
