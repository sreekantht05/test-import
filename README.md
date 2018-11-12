@Sree, @Shub, and @Sheryll to update based on the format example below, thanks!


 REFERENCE
https://github.com/sfdcit/aws-tf-lib/tree/v0.0.0/modules/environments/name-prefix
## What It Does
We have a naming standard that includes prefixes to indicate the environment of an AWS resource. It is inefficient to have individual programmers hand type the prefixes. This module can create name prefixes for global resources, regional resources, or resources shared from another project. Lastly, this module can add a developer username to the prefix, so that developers can provision resources that has their name on it.  For global and regional prefix standards, see our [AWS Resources Naming Standards](https://docs.google.com/document/d/1jdgicHm7ZQYjLhbgPTt40EGmoumM2ds7JrZA_nZW0FU/edit).
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



# Use this template to create your repos in sfdcit org using CLI

1. Clone \
   git clone https://github.com/sfdcit/aws-tf-proj-template.git
2. Make executable \
   chmod 700 github-create.sh
3. Run script along with project name as parameter \
   sh github-create.sh {project name} \
   ex. sh github-create.sh aws-tf-proj-vmdec 
4. Your repo should be created and is pushed to dev branch
   
