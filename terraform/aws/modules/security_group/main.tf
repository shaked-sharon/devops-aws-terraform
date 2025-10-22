# Security Group Module
# Creates SG > relative VPC
# Inbound: TCP 22 (SSH) & TCP 5001 (app)
# Outbound: all

resource "aws_security_group" "this" {
  name_prefix = var.name_prefix
  description = var.description
  vpc_id      = var.vpc_id
}

# Inbound SSH (22)
resource "aws_security_group_rule" "ssh_in" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = var.allowed_cidrs
  security_group_id = aws_security_group.this.id
  description       = "SSH"
}

# Inbound App (5001)
resource "aws_security_group_rule" "app_in" {
  type              = "ingress"
  from_port         = 5001
  to_port           = 5001
  protocol          = "tcp"
  cidr_blocks       = var.allowed_cidrs
  security_group_id = aws_security_group.this.id
  description       = "App port 5001"
}

# Outbound: allow all
resource "aws_security_group_rule" "egress_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.this.id
  description       = "Allow all outbound"
}
