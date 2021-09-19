# API Gateway Infrastructure

## HTTP API
resource "aws_apigatewayv2_api" "main" {
  depends_on    = [aws_lambda_function.app]
  name          = "${terraform.workspace}-${var.project_name}"
  protocol_type = "HTTP"
  description   = "${var.project_name} deployment"

  tags = {
    DeployedBy  = "terraform"
    Project     = var.project_name
    ProjectURL  = var.project_url
    Environment = terraform.workspace
  }

}

## CloudWatch Log Group to store logs of API requests
resource "aws_cloudwatch_log_group" "main" {
  name = "${terraform.workspace}-${var.project_name}"

  tags = {
    DeployedBy  = "terraform"
    Project     = var.project_name
    ProjectURL  = var.project_url
    Environment = terraform.workspace
  }

}

## HTTP API Stage
resource "aws_apigatewayv2_stage" "stage" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = terraform.workspace
  auto_deploy = terraform.workspace == "dev" ? true : false
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.main.arn
    format          = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      caller         = "$context.identity.caller"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      resourcePath   = "$context.resourcePath"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseLength = "$context.responseLength"
    })

  }

  tags = {
    DeployedBy  = "terraform"
    Project     = var.project_name
    ProjectURL  = var.project_url
    Environment = terraform.workspace
  }

}

## Lambda Integration
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.main.id
  integration_type = "AWS_PROXY"
  connection_type  = "INTERNET"
  description      = "${var.project_name} lambda function."
  integration_uri  = aws_lambda_function.app.invoke_arn
}

## HTTP PUT Route
resource "aws_apigatewayv2_route" "put_route" {
  api_id              = aws_apigatewayv2_api.main.id
  route_key           = "PUT /hello/{username}"
  target              = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  authorization_type  = "NONE"
}

## HTTP GET Route
resource "aws_apigatewayv2_route" "get_route" {
  api_id              = aws_apigatewayv2_api.main.id
  route_key           = "GET /hello/{username}"
  target              = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  authorization_type  = "NONE"
}

# HTTP Default Route
resource "aws_apigatewayv2_route" "default_route" {
  api_id              = aws_apigatewayv2_api.main.id
  route_key           = "$default"
  target              = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  authorization_type  = "NONE"
}

resource "aws_apigatewayv2_deployment" "main" {

  depends_on = [ 
    aws_apigatewayv2_route.put_route, 
    aws_apigatewayv2_route.get_route, 
    aws_apigatewayv2_route.default_route
  ]

  api_id      = aws_apigatewayv2_api.main.id
  description = "${var.project_name} deployment"

  lifecycle {
    create_before_destroy = true
  }
}