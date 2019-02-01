output "service-role-arn" {
  value = "${module.ssprod-or.service-role-arn}"
}

output "lambda-arn" {
  value = "${module.ssprod-or.lambda-arn}"
}

output "cloudwatch-arn" {
  value = "${module.ssprod-or.cloudwatch-arn}"
}
