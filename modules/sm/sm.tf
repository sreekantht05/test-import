locals {
  secret_name = "${var.regional_prefix}-secretsmanager-${var.service_target}${var.name_suffix == "x" ? "" : "-${var.name_suffix}"}"
}

resource "aws_secretsmanager_secret" "asset_mgmt_secret" {
  name        = "${local.secret_name}"
  description = "Secret manager to store encrypted sf credentials"
  kms_key_id  = "${var.key_arn}"
}

resource "aws_secretsmanager_secret_version" "asset_mgmt_secret_version" {
  secret_id     = "${aws_secretsmanager_secret.asset_mgmt_secret.id}"
  secret_string = "${jsonencode(var.secret)}"
}

#------------------------------------------------------
#Outputs
#------------------------------------------------------

output "secret_name" {
  value = "${aws_secretsmanager_secret.asset_mgmt_secret.name}"
}
