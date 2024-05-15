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

variable "bucket_name" {
  type = string
}

# referencing the latest zip in s3 with version id
data "aws_s3_object" "layerzip" {
  bucket = var.bucket_name # "bucket-test-777"
  key    = "hana-test/XlsWriter.zip"
}

# create lambda layer with latest zip in s3 can be used even for update cause there will be tfstate store in s3 and it will differentiate the object version id
resource "aws_lambda_layer_version" "hanalayer" {
  s3_bucket           = var.bucket_name
  s3_key              = "hana-test/XlsWriter.zip"
  s3_object_version   = data.aws_s3_object.layerzip.version_id
  layer_name          = "hanalayer"
  compatible_runtimes = ["python3.9"]
  skip_destroy        = true
}

#terraform backend configuration, save into the s3 bucket
terraform {
  backend "s3" {
    bucket         = "tfstatehana"
    key            = "terraform.tfstate"
    region         = "ap-southeast-1"  # Replace with your desired region
  }
}
