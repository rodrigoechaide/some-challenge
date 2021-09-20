# Lambda Infrastructure

data "aws_caller_identity" "current" {}

resource "aws_iam_role" "app" {
  name = "${terraform.workspace}-${var.project_name}"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF

  tags = {
    DeployedBy  = "terraform"
    Project     = var.project_name
    ProjectURL  = var.project_url
    Environment = terraform.workspace
  }

}

resource "aws_iam_policy" "app" {
  name        = "${terraform.workspace}-${var.project_name}"
  path        = "/"
  description = "IAM policy for ${terraform.workspace}-${var.project_name} lambda function"
  policy      = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CloudWatchLogsAccessPermissions",
      "Effect": "Allow",
      "Action": [
        "logs:PutLogEvents",
        "logs:CreateLogStream",
        "logs:CreateLogGroup"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DynamoDBTableAccessPermissions",
      "Effect": "Allow",
      "Action": [
        "dynamodb:BatchGetItem",
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:BatchWriteItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem"
      ],
      "Resource": "arn:aws:dynamodb:${var.region}:${data.aws_caller_identity.current.account_id}:table/${terraform.workspace}_${var.dynamodb_table_name}"
    }
  ]
}
EOF

  tags = {
    DeployedBy  = "terraform"
    Project     = var.project_name
    ProjectURL  = var.project_url
    Environment = terraform.workspace
  }

}

resource "aws_iam_role_policy_attachment" "app" {
  role       = aws_iam_role.app.name
  policy_arn = aws_iam_policy.app.arn
}

data "archive_file" "app" {
  type        = "zip"
  source_dir  = "../hello/app/"
  excludes    = [ "requirements.txt", "__pycache__" ]
  output_path = "../hello/app.zip"
}

resource "aws_lambda_function" "app" {
  filename      = "../hello/app.zip"
  function_name = "${terraform.workspace}-${var.project_name}"
  role          = aws_iam_role.app.arn
  handler       = "main.lambda_handler"
  timeout       = var.lambda_timeout
  source_code_hash = data.archive_file.app.output_base64sha256
  runtime = "python3.9"

  environment {
    variables = {
      ENVIRONMENT = terraform.workspace
      TABLE_NAME  = "${terraform.workspace}_${var.dynamodb_table_name}"
    }
  }

  tags = {
    DeployedBy  = "terraform"
    Project     = var.project_name
    ProjectURL  = var.project_url
    Environment = terraform.workspace
  }

}

resource "aws_lambda_permission" "apigateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.app.function_name}"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}