terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-1"
}

# create lambda layer from s3 object
resource "aws_lambda_layer_version" "my-lambda-layer" {
  s3_bucket           = bucket-test-777
  s3_key              = hana-test/XlsWriter.zip
  layer_name          = hanalayer
  compatible_runtimes = ["python3.11"]
  skip_destroy        = true
}

# try to reference it with latest arn
data "aws_lambda_layer_version" "mylatest" {
  layer_name = aws_lambda_layer_version.my-lambda-layer.layer_name
}

resource "aws_lambda_function" "hanalambda" {
  function_name = "hanalambda"
  handler      = "index.handler"
  runtime      = "python3.11"
  layers       = [data.aws_lambda_layer_version.mylatest.arn]
  # other configuration options
}
