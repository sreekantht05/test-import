variable "default_region" {
  description = "the AWS region that should create the IAM resources"
  default     = "us-west-2"
}

variable "asset_lambda_create" {
  default     = true
  description = "Enable Lambda function Creation"
}
