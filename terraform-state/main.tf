resource "aws_s3_bucket" "tf_backend_bucket" {
  bucket = var.bucket_name
  acl    = "private"
  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DenyDeletBucketOperation",
            "Effect": "Deny",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:DeleteBucket",
            "Resource": "arn:aws:s3:::${var.bucket_name}"
        }
    ]
}
POLICY

  versioning {
    enabled = true
  }

  tags = {
      DeployedBy = "terraform"
      Project    = "some-challenge"
      ProjectURL = "https://github.com/rodrigoechaide/some-challenge"
  }

}

resource "aws_s3_bucket_public_access_block" "tf_backend_bucket" {
  bucket = aws_s3_bucket.tf_backend_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "tf_lock_table" {
  name           = var.dynamodb_table_name
  read_capacity  = 5
  write_capacity = 1
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
      DeployedBy = "terraform"
      Project    = "some-challenge"
      ProjectURL = "https://github.com/rodrigoechaide/some-challenge"
  }
}