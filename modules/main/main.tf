module "envcode" {
  source = "git@github.com:sfdcit/aws-tf-lib.git//modules/environments/envcode?ref=v1.0.0"
}

module "tags" {
  source          = "git@github.com:sfdcit/aws-tf-lib.git//modules/environments/tags?ref=v1.0.0"
  technology      = "${var.technology}"
  technology_code = "${var.technology_code}"
  created_by      = "${var.created_by}"
}

module "name-prefix" {
  source          = "git@github.com:sfdcit/aws-tf-lib.git//modules/environments/name-prefix?ref=v1.0.0"
  envcode         = "${module.envcode.envcode}"
  regcode         = "${module.envcode.regcode}"
  technology_code = "${module.tags.tagmap["TechnologyCode"]}"
}

module "gitrepo-cwlambda-role" {
  source         = "git@github.com:sfdcit/aws-tf-lib.git//modules/security/role/service-role?ref=v1.0.0"
  default_region = "${var.default_region}"
  global_prefix  = "${module.name-prefix.global_prefix}"
  service        = "lambda.amazonaws.com"
  role_purpose   = "cwlambda"

  # Inline policy variables
  inline_policy  = true
  policy_purpose = "cwlambda"
  sid_list       = ["lambdaexecAccess", "EC2ReadAccess", "SecretsAccess", "cloudwatchAccess", "AllowKMSAccess"]
  effect_list    = ["Allow", "Allow", "Allow", "Allow", "Allow"]
  actions_list   = ["lambda:InvokeFunction", "ec2:CreateNetworkInterface,ec2:DeleteNetworkInterface,ec2:AttachNetworkInterface,ec2:DetachNetworkInterface,ec2:DescribeNetworkInterfaces", "secretsmanager:GetResourcePolicy,secretsmanager:GetSecretValue,secretsmanager:DescribeSecret", "cloudwatch:Describe*,cloudwatch:Get*,cloudwatch:List*,logs:CreateLogStream,logs:DeleteLogStream,logs:Get*,logs:List*,logs:Describe*,logs:TestMetricFilter,logs:FilterLogEvents,logs:CreateLogGroup,logs:Put*", "kms:ReEncrypt*,kms:GenerateDataKey*,kms:Encrypt,kms:DescribeKey,kms:Decrypt"]
  resources_list = ["*"]
  tagmap         = "${module.tags.tagmap}"
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
  source           = "git@github.com:sfdcit/aws-tf-lib.git//modules/compute/lambda/function/vpc-access?ref=v1.0.0"
  regional_prefix  = "${module.name-prefix.regional_prefix}"
  function_purpose = "cwlambda"
  function_source  = "../../modules/lambda_python_code"
  function_runtime = "python3.6"
  function_timeout = "300"
  key_arn          = ""

  function_subnet_ids = "${data.aws_subnet.private_subnets.*.id}"
  function_sg_ids     = ["${data.aws_security_group.admin_sgs.*.id}", "${data.aws_security_group.http_sgs.*.id}"]

  function_handler = "lambda_function.lambda_handler"
  role_arn         = "${module.gitrepo-cwlambda-role.role_arn}"

  function_trigger_principal = "events.amazonaws.com"
  function_trigger_arn       = "${module.cloudwatch.event_arn}"

  environment_variables = {
    secret_name = "${var.secret_name}"
  }

  tags = "${module.tags.tagmap}"
}

module "cloudwatch" {
  source              = "git@github.com:sfdcit/aws-tf-lib.git//modules/monitoring/cw-event?ref=v1.0.0"
  regional_prefix     = "${module.name-prefix.regional_prefix}"
  name                = "cw-schedule"
  event_purpose       = "Cloud watch Scheduler to ensure the branch protection rules are intact for git repository"
  role_arn            = ""
  target_purpose      = "cw-schedule"
  target_arn          = "${module.lambda.function_arn}"
  schedule_expression = "rate(1 hour)"
}

data "aws_iam_policy_document" "gitrepolambda_invoke_doc" {
  statement {
    sid    = "InvokeLambda"
    effect = "Allow"

    resources = [
      "${module.lambda.function_arn}",
    ]

    actions = [
      "lambda:InvokeFunction",
      "lambda:InvokeAsync",
    ]
  }
}

resource "aws_iam_policy" "gitrepolambda_invoke" {
  lifecycle {
    prevent_destroy = true
  }

  description = "Allow Lambda InvokeFunction access for ssprod-or-grepo-function-cwlambda function"
  name        = "${module.name-prefix.regional_prefix}-policy-gitrepolambdainvoke"
  policy      = "${data.aws_iam_policy_document.gitrepolambda_invoke_doc.json}"
}

data "aws_iam_group" "infradev" {
  group_name = "${var.group_name}"
}

resource "aws_iam_group_policy_attachment" "infradev_group_attach" {
  group      = "${data.aws_iam_group.infradev.group_name}"
  policy_arn = "${aws_iam_policy.gitrepolambda_invoke.arn}"
}

data "aws_iam_role" "infradev" {
  name = "${var.role_name}"
}

resource "aws_iam_role_policy_attachment" "infradev_group_attach" {
  role       = "${data.aws_iam_role.infradev.name}"
  policy_arn = "${aws_iam_policy.gitrepolambda_invoke.arn}"
}
