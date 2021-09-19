variable "dynamodb_table_name" {
  type        = string
  description = "Table name for the DynamoDB table for state locking."
}

variable "region" {
  type        = string
  description = "AWS Region to deploy the Infrastructure"
}

variable "project_name" {
  type        = string
  description = "Project Name"
}

variable "project_url" {
  type        = string
  description = "Project URL"
}

variable "lambda_timeout" {
  type        = string
  description = "Lambda Timeout Parameter"
  default     = "15"
}