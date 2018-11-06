module "envcode" {
  source = "git@github.com:sfdcit/aws-tf-lib.git//modules/environments/envcode"
}

module "tags" {
  source          = "git@github.com:sfdcit/aws-tf-lib.git//modules/environments/tags"
  created_by      = "aws-tf-proj-template repo"
  technology      = "Git repo creation"
  technology_code = "grepo"
}

module "name-prefix" {
  source          = "git@github.com:sfdcit/aws-tf-lib.git//modules/environments/name-prefix"
  envcode         = "${module.envcode.envcode}"
  regcode         = "${module.envcode.regcode}"
  technology_code = "${module.tags.tagmap["TechnologyCode"]}"
}

module "gitrepo-cwlambda-role" {
  source         = "git@github.com:sfdcit/aws-tf-lib.git//modules/security/role/service-role"
  default_region = "${var.default_region}"
  global_prefix  = "${module.name-prefix.global_prefix}"
  service        = "lambda.amazonaws.com"
  role_purpose   = "cwsqslambda"

  # Inline policy variables
  inline_policy  = true
  policy_purpose = "sqswrite"
  sid_list       = ["GetCloudWatchAlarms"]
  effect_list    = ["Allow"]

  actions_list = [
    "ec2:CreateNetworkInterface,ec2:DeleteNetworkInterface,ec2:AttachNetworkInterface,ec2:DetachNetworkInterface,ec2:DescribeNetworkInterfaces,secretsmanager:GetResourcePolicy,secretsmanager:GetSecretValue,secretsmanager:DescribeSecret,cloudwatch:Describe*,cloudwatch:Get*,cloudwatch:List*,logs:CreateLogStream,logs:DeleteLogStream,logs:Get*,logs:List*,logs:Describe*,logs:TestMetricFilter,logs:FilterLogEvents,logs:CreateLogGroup,logs:Put*,kms:ReEncrypt*,kms:GenerateDataKey*,kms:Encrypt,kms:DescribeKey,kms:Decrypt",
  ]

  resources_list = ["*"]
}

module "project-key" {
  source          = "git@github.com:sfdcit/aws-tf-lib.git//modules/security/kms"
  regional_prefix = "${module.name-prefix.regional_prefix}"
  tagmap          = "${module.tags.tagmap}"
  services        = ["lambda.amazonaws.com"]
}

data "aws_vpc" "foundation_vpc" {
  count = "${var.asset_lambda_create}"

  filter = {
    "name"   = "tag:Name"
    "values" = ["*-fundn-vpc-*"]
  }
}

# Get a list of availability zones in the current region
data "aws_availability_zones" "az" {}

// Get a list of private subnets in the Foundation VPC
data "aws_subnet" "private_subnets" {
  count = "${var.asset_lambda_create ? 3:0}"

  vpc_id            = "${data.aws_vpc.foundation_vpc.0.id}"
  availability_zone = "${element(data.aws_availability_zones.az.names, count.index)}"

  filter = {
    "name"   = "tag:Name"
    "values" = ["*-private"]
  }
}

data "aws_security_group" "admin_sgs" {
  count = "${var.asset_lambda_create}"

  vpc_id = "${data.aws_vpc.foundation_vpc.0.id}"

  filter {
    name   = "tag:Name"
    values = ["*fundn-sg-default-admin"]
  }
}

data "aws_security_group" "http_sgs" {
  count = "${var.asset_lambda_create}"

  vpc_id = "${data.aws_vpc.foundation_vpc.0.id}"

  filter {
    name   = "tag:Name"
    values = ["*asset-sg-sf"]
  }
}

module "lambda" {
  source             = "../../modules/lambda"
  regional_prefix    = "${module.name-prefix.regional_prefix}"
  function_purpose   = "cwlambda"
  function_source    = "../../modules/lambda_python_code"
  handler            = "lambda_function"
  cloudwatch_arn     = "${module.cloudwatch.arn}"
  runtime            = "python3.6"
  role               = "${module.gitrepo-cwlambda-role.role_arn}"
  subnet_ids         = "${data.aws_subnet.private_subnets.*.id}"
  security_group_ids = ["${data.aws_security_group.admin_sgs.*.id}", "${data.aws_security_group.http_sgs.*.id}"]
  secret_name        = "${module.sm.secret_name}"
}

module "cloudwatch" {
  source          = "../../modules/cloudwatch"
  regional_prefix = "${module.name-prefix.regional_prefix}"
  target_arn      = "${module.lambda.arn}"
}

module "sm" {
  source          = "../../modules/sm"
  envcode         = "${module.envcode.envcode}"
  tagmap          = "${module.tags.tagmap}"
  regional_prefix = "${module.name-prefix.regional_prefix}"
  service_target  = "github"
  key_arn         = "${module.project-key.key_alias_arn}"

  secret {
    token = "dummy_replace_encrypted_value"
  }
}
