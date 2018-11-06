resource "aws_cloudwatch_event_rule" "gitrepo" {
  name                = "${var.regional_prefix}-cw-ec2-gitrepo"
  description         = "Cloud watch Scheduler to ensure the branch protection rules are intact for git repository"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "gitrepo_cw_lambda" {
  rule = "${aws_cloudwatch_event_rule.gitrepo.name}"
  arn  = "${var.target_arn}"
}

output "arn" {
  value = "${aws_cloudwatch_event_rule.gitrepo.arn}"
}
