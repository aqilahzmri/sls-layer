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

# referencing the latest zip with version id
data "aws_s3_object" "layerzip" {
  bucket = "bucket-test-777"
  key    = "hana-test/XlsWriter.zip"
}

# create lambda layer from s3 object
resource "aws_lambda_layer_version" "hanalayer" {
  s3_bucket           = data.aws_s3_object.layerzip.id
  s3_key              = data.aws_s3_object.layerzip.key
  s3_object_version   = data.aws_s3_object.layerzip.version_id
  layer_name          = "hanalayer"
  compatible_runtimes = ["python3.9"]
  skip_destroy        = true
}

# try to reference it with latest arn
data "aws_lambda_layer_version" "mylatest" {
  layer_name = aws_lambda_layer_version.hanalayer.layer_name
}

#terraform backend configuration, save into the s3 bucket
terraform {
  backend "s3" {
    bucket         = "tfstatehana"
    key            = "terraform.tfstate"
    region         = "ap-southeast-1"  # Replace with your desired region
  }
}
