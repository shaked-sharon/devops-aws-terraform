variable "key_name" {
  description = "Name of EC2 key pair"
  type        = string
  default     = "devops-key"
}

variable "public_key_path" {
  description = "Path for Public SSH key .pub"
  type        = string
  default     = "~/.ssh/devops-key.pub"
}

variable "instance_name" {
  description = "Instance Name Tag"
  type        = string
  default     = "devops-ec2"
}

variable "instance_type" {
  description = "EC2 Instance Type"
  type        = string
  default     = "t3.micro"
}

variable "allowed_cidrs" {
  description = "CIDR blocks authorized for inbound ports in Security Group"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "user_data" {
  description = "Cloud init scripts--not required"
  type        = string
  default     = ""
}