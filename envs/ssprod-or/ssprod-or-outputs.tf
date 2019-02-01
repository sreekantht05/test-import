output "service-role-arn" {
  value = "${module.ssprod.service-role-arn}"
}

output "lambda-arn" {
  value = "${module.ssprod.lambda-arn}"
}

output "cloudwatch-arn" {
  value = "${module.ssprod.cloudwatch-arn}"
}
