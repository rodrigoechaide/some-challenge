variable "bucket_name" {
  type        = string
  description = "Bucket name for the s3 bucket where terraform state files are going to be stored."
}

variable "dynamodb_table_name" {
  type        = string
  description = "Table name for the DynamoDB table for state locking."
}