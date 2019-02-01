output "service-role-arn" {
  value = "${module.ssdev.service-role-arn}"
}

output "lambda-arn" {
  value = "${module.ssdev.lambda-arn}"
}

output "cloudwatch-arn" {
  value = "${module.ssdev.cloudwatch-arn}"
}
