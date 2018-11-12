locals {
  function_name = "${var.regional_prefix}-function-${var.function_purpose}"
}

data "archive_file" "gitrepo_cw" {
  type        = "zip"
  source_dir  = "${var.function_source}"
  output_path = "${local.function_name}.zip"
}

resource "aws_lambda_function" "lambda" {
  filename         = "${local.function_name}.zip"
  function_name    = "${local.function_name}"
  role             = "${var.role}"
  handler          = "${var.handler}.lambda_handler"
  source_code_hash = "${data.archive_file.gitrepo_cw.output_base64sha256}"
  runtime          = "${var.runtime}"
  timeout          = 120

  vpc_config {
    subnet_ids         = ["${var.subnet_ids}"]
    security_group_ids = ["${var.security_group_ids}"]
  }

  environment {
    variables = {
      secret_name = "${var.secret_name}"
    }
  }
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.lambda.function_name}"
  principal     = "events.amazonaws.com"
  source_arn    = "${var.cloudwatch_arn}"
}

output "name" {
  value = "${aws_lambda_function.lambda.function_name}"
}

output "arn" {
  value = "${aws_lambda_function.lambda.arn}"
}
