output "tf_backend_bucket_name" {
  description = "The backend bucket name."
  value       = aws_s3_bucket.tf_backend_bucket.id
}

output "tf_lock_table_name" {
  description = "DynamoDB lock table name"
  value       = aws_dynamodb_table.tf_lock_table.id
}