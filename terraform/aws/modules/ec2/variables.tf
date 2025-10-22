# Input > EC2 module
variable "subnet_id" {
  description = "Subnet ID for instance"
  type        = string
}

variable "security_group_ids" {
  description = "Lists Security Group ID"
  # note from class: use 'any' list
  type = list(any)
}

variable "instance_type" {
  description = "EC2 Instance Type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Name of EC2 Key Pair"
  type        = string
  default     = null
}

variable "name" {
  description = "Instance Name Tag"
  type        = string
  default     = "devops-ec2"
}

variable "user_data" {
  description = "Cloud Initialization Script"
  type        = string
  default     = ""
}

variable "common_tags" {
  description = "Extra tags merged with Name"
  type        = map(any)
  default     = {}
}
