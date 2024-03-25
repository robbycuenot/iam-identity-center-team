# Terraform cloud workspace config
terraform {
  required_version = ">= 1.7.0"
  backend "remote" {
    organization = "ExampleOrganization"
    workspaces {
      name = "ExampleWorkspace"
    }
  }
}

provider "aws" {
  region = var.AWS_REGION
}
