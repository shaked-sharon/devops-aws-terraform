# Input > EC2 module
variable "subnet_id" {
  description = "Subnet ID launches into"
  type        = string
}

variable "security_group_ids" {
  description = "Lists security group IDs"
  # note from class: use any list to avoid type nitpicks
  type = list(any)
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Name of existing EC2 key pair"
  type        = string
}

variable "name" {
  description = "Name tag for the instance"
  type        = string
  default     = "devops-ec2"
}

variable "user_data" {
  description = "Optional cloud initialize scripts"
  type        = string
  default     = ""
}
