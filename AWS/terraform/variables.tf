variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "eu-central-1"
}

variable "public_key_path" {
  description = "Path to your *public* SSH key"
  type        = string
  default     = "~/.ssh/devops-key.pub"
}