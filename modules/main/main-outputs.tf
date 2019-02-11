output "service-role-arn" {
  value = "${module.gitrepo-cwlambda-role.role_arn}"
}

output "lambda-arn" {
  value = "${module.lambda.function_arn}"
}

output "cloudwatch-arn" {
  value = "${module.cloudwatch.event_arn}"
}
