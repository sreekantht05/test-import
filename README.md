## Terraform GIT Repo Module

## What It Does
This Module creates AWS resources which creates a GIT Repository along with some branches, .gitignore file, CODEOWNERS file and folders with a predefined hierarchy.
 - Master branch is removed, dev or ssdev is marked as default branch depending upon the requirement.
 - All the branches that are specified are branch protected and able to merge via pull requests.
 - Teams or owners that are specified  are added into the CODEOWNERS file.
 - This module also creates a cloudwatch rule which runs daily to check branch protection for all the repositories in "sfdcit" organisation

## Module Limitations
- The *lambda* needs vpc, subnets and security_groups created by *fundn* repository as well as *asset management* repository.
- The *lambda* reuses the secret that already created in secretsmanager - "aws-tf-proj-plan_alert-github_token"

 ## How to use It
### Standalone Example
```hcl
 module "ssdev" {
  source = "../../modules/main"
  # Global Tags
  technology = "Git Repository"
  technology_code = "grepo"
  created_by      = "aws-tf-proj-gitrepo"

  # lambda variables
  secret_name = "aws-tf-proj-plan_alert-github_token"
}
```
 
 ## Required Variables
- **envcode:** A short-name of an AWS account that is supported by IT. Valid values are *sbx*, *dev*, *ssdev*, *qa*, *uat*, *prod*, *ssprod*, *soxprod*, *dr*, and *soxdr*. For an updated list, reference the [README for Envcode module](../envcode/README.md).
   
- **regcode:** A two-character code of the AWS Region where an AWS resource resides. Valid values are *or*, *va*, *oh*, *ie*, *dd*, *fr*, *sg*, *au*, and *in*. For an updated list, reference the [README for Envcode module](../envcode/README.md).
 --------

