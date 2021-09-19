provider "aws" {
  region  = var.region
}

terraform {
  required_version = "~> 1"

  backend "s3" {
    bucket         = "some-challenge-tf-backend"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "some-challenge-tf-lock-table"
  }

  required_providers {
     aws = {
       source = "hashicorp/aws"
       version = "~> 3.0"
     }
  }
}