variable "vpc_id" {
  description = "ID of VPC where security group will be generated"
  type        = string
}

variable "name_prefix" {
  description = "Prefix for security group name"
  type        = string
  default     = "devops-sg"
}

variable "description" {
  description = "Description of security group"
  type        = string
  default     = "Allow SSH (22) & app (5001)"
}

variable "allowed_cidrs" {
  description = "CIDR blocks auth to access inbound ports"
  type        = list(string)
  default     = ["0.0.0.0/0"] # WARNING!!: public/open > all; okay for class/demo, NOT prod!!
}
