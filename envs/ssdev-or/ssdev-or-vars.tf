module "ssdev" {
  source = "../../modules/main"

  #------------------------------------------------------
  # Global Tags
  #------------------------------------------------------
  technology = "Git Repository"

  technology_code = "grepo"
  created_by      = "aws-tf-proj-gitrepo"

  # lambda variables
  secret_name = "aws-tf-proj-plan_alert-github_token"
  group_name  = "ssdev-fundn-group-infradev"
}
