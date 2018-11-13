## Terraform GIT Repo Module

## What It Does
This Module creates AWS resources which creates a GIT Repository along with some branches, .gitignore file, CODEOWNERS file and folders with a predefined hierarchy.
 - Master branch is removed, dev or ssdev is marked as default branch depending upon the requirement.
 - All the branches that are specified are branch protected and able to merge via pull requests.
 - Teams or owners that are specified  are added into the CODEOWNERS file.
 - This module also creates a cloudwatch rule which runs daily to check branch protection for all the repositories in "sfdcit" organisation

## Module Limitations
- The *global_prefix* output only includes the {Environment} and the {Technology} codes described in the naming standard.
- The *regional_prefix* output only includes the {Environment}, {Region}, and {Technology} codes described in the naming standard.
- The *environment_prefix* output only includes the {Environment} and {Region} codes described in the naming standard.
- The *developer_username* input only adds to the *global_prefix* and *regional_prefix* outputs. The *environment_prefix* output is not affected.
 ## How to use It
### Standalone Example
```hcl
module "name-prefix" {
  source = "git@github.com:sfdcit/aws-tf-lib.git//modules/environments/name-prefix"
   envcode            = "dev"
  regcode            = "or"
  technology_code    = "confl"
  developer_username = "pvuong"
}
```
 ### Combine with Envcode and Tags modules
```hcl
 locals {
  tech_code = "confl"
  tech_name = "Confluence"
  repo_name = "aws-tf-proj-confl repo"
}
 module "envcode" {
  source = "git@github.com:sfdcit/aws-tf-lib.git//modules/environments/envcode"
}
 module "tags" {
  source = "git@github.com:sfdcit/aws-tf-lib.git//modules/environments/tags"
   technology      = "${local.tech_name}"
  technology_code = "${local.tech_code}"
  created_by      = "${local.repo_name}"
}
 module "name-prefix" {
  source = "git@github.com:sfdcit/aws-tf-lib.git//modules/environments/name-prefix"
   envcode            = "${module.envcode.envcode}"
  regcode            = "${module.envcode.regcode}"
  technology_code    = "${local.tech_code}"
  developer_username = "${var.developer_username}"
}
```
 ## Required Variables
- **envcode:** A short-name of an AWS account that is supported by IT. Valid values are *sbx*, *dev*, *ssdev*, *qa*, *uat*, *prod*, *ssprod*, *soxprod*, *dr*, and *soxdr*. For an updated list, reference the [README for Envcode module](../envcode/README.md).
   
- **regcode:** A two-character code of the AWS Region where an AWS resource resides. Valid values are *or*, *va*, *oh*, *ie*, *dd*, *fr*, *sg*, *au*, and *in*. For an updated list, reference the [README for Envcode module](../envcode/README.md).
 --------

