# DynamoDB Infrastructure

## DynamoDB Table
resource "aws_dynamodb_table" "backend_table" {
  name           = "${terraform.workspace}_${var.dynamodb_table_name}"
  read_capacity  = 5
  write_capacity = 1
  hash_key       = "username"

  attribute {
    name = "username"
    type = "S"
  }

  tags = {
    DeployedBy  = "terraform"
    Project     = var.project_name
    ProjectURL  = var.project_url
    Environment = terraform.workspace
  }
}