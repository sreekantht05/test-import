output "service-role-arn" {
  value = "${module.ssdev-or.service-role-arn}"
}

output "lambda-arn" {
  value = "${module.ssdev-or.lambda-arn}"
}

output "cloudwatch-arn" {
  value = "${module.ssdev-or.cloudwatch-arn}"
}
