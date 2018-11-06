variable "regional_prefix" {
  description = "name prefix that will be the beginning of the function name."
  type        = "string"
}

variable "function_purpose" {
  type        = "string"
  description = "Short description of the lambda function. This value will be appended to the end of the function name."
}

variable "function_source" {
  type        = "string"
  description = "The path to the source folder for the lambda function."
}

variable "cloudwatch_arn" {
  description = "arn of the cloud watch for event source mapping"
}

variable "runtime" {
  description = "The runtime of the lambda to create"
  default     = "python"
}

variable "handler" {
  description = "The handler name of the lambda (a function defined in your lambda)"
}

variable "role" {
  description = "IAM role attached to the Lambda Function (ARN)"
}

variable "subnet_ids" {
  default = []
}

variable "security_group_ids" {
  default = []
}

variable "secret_name" {
  description = "environment variable for providing the secret name"
}
