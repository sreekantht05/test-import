variable "envcode" {}

variable "regional_prefix" {}

variable "tagmap" {
  type = "map"
}

variable "service_target" {
  description = "The AWS service name that will use this secret (e.g. rds, ec2)"
  type        = "string"
}

variable "name_suffix" {
  description = "The ability to add a suffix to the secret_name due to minimum 7 day reuse of name. Add in increments of 'x' if not used. Change this value to anything else if used."
  type        = "string"
  default     = "x"
}

variable "key_arn" {
  description = "Specifies the ARN or alias of the AWS KMS customer master key (CMK) to be used to encrypt the secret values in the versions stored in this secret"
  type        = "string"
  default     = ""
}

variable "secret" {
  description = "The contains the encrypted secret of sf credentials"
  type        = "map"
}
