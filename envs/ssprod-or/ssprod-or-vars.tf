module "ssprod-or" {
  source = "../../modules/main"

  # lambda variables
  secret_name        = "aws-tf-proj-plan_alert-github_token"
  group_name         = "ssprod-fundn-group-infradev"
  role_name          = "ssprod-fundn-role-infradev"
  infraops_role_name = "ssprod-fundn-role-infraops"
}
