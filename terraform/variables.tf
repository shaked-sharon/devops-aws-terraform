variable "region" {
  type    = string
  default = "eu-central-1"
}

variable "instance_type" {
  type    = string
  default = "t3.medium"
}

variable "key_name" {
  type    = string
  default = "builder-key"
}

variable "private_key_path" {
  type    = string
  default = "./builder_key.pem"
}

variable "home_cidr" {
  type = string
}

variable "open_world_port" {
  type    = number
  default = 5001
}

variable "name_prefix" {
  type    = string
  default = "builder"
}