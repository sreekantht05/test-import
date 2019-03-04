#--------------------------------------------
# Tag Variables
#--------------------------------------------

variable "technology" {
  type        = "string"
  description = "Technology name from Supportforce Technologies object"
  default     = "Git Repository"
}

variable "technology_code" {
  type        = "string"
  description = "Technology-Code from Supportforce IT Applications object"
  default     = "grepo"
}

variable "created_by" {
  type        = "string"
  description = "Location of the source code"
  default     = "aws-tf-proj-grepo"
}

variable "default_region" {
  description = "the AWS region that should create the IAM resources"
  default     = "us-west-2"
}

variable "asset_lambda_create" {
  default     = true
  description = "Enable Lambda function Creation"
}

#--------------------------------------------
# lambda Variables
#--------------------------------------------
variable "secret_name" {
  type        = "string"
  description = "Secret name to retrieve the github token"
}

#--------------------------------------------
# Infradev policy variables
#--------------------------------------------
variable "group_name" {
  type        = "string"
  description = "Infradev Group Name"
}

variable "role_name" {
  type        = "string"
  description = "Infradev Role Name"
}

variable "infraops_role_name" {
  type        = "string"
  description = "Infraops Role Name"
}
