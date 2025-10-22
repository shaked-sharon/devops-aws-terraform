terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "shaked-s3-devops"     # AWS S3 bucket name
    key    = "terraform/state.tfstate"
    region = "us-east-2"
  }
}

provider "aws" {
  region = "us-east-2"

  default_tags {
    tags = {
      env   = "devops"
      owner = "Sharon"
    }
  }
}