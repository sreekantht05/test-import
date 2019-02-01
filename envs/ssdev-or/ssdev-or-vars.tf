module "ssdev-or" {
  source = "../../modules/main"

  # lambda variables
  secret_name = "aws-tf-proj-plan_alert-github_token"
  group_name  = "ssdev-fundn-group-infradev"
  role_name   = "ssdev-fundn-role-infradev"
}
