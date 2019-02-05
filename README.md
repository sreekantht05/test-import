## Terraform GIT Repo Module

## What It Does
This Module creates AWS resources which creates a GIT Repository along with some branches, .gitignore file, CODEOWNERS file and folders with a predefined hierarchy.
 - Master branch is removed, dev or ssdev is marked as default branch depending upon the requirement.
 - All the branches that are specified are branch protected and able to merge via pull requests.
 - Teams or owners that are specified  are added into the CODEOWNERS file.
 - This module also creates a cloudwatch rule which runs daily to check branch protection for all the repositories in "sfdcit" organisation.
 - Staus checks are enabled for the terraform plan for branches to ensure that only successfull terraform plans are allowed to merge.

## Module Limitations
- The *lambda* needs vpc, subnets and security_groups created by *fundn* repository as well as *asset management* repository.
- The *lambda* reuses the secret that already created in secretsmanager - "aws-tf-proj-plan_alert-github_token"
- This modules creates only "Oregon" region specific directories under "envs" directory.(e.g. "envs/dev-or/dev-or-vars.tf"). For other regions user needs to create the directories.

 ## How to use It : Frontend
#### Prerequisite
  User need to login to "SSProd" AWS Account via "awslogin" script before running the "create_repo.py" script.
  
 ### New GitHub Repository Creation
  Run [create_repo.py](https://github.com/sfdcit/aws-tools/tree/master/devtools) from your local machine to create new Github repository. To have the best user experience, Python 3 is preferred. To download and install Python 3, please download a stable version from https://www.python.org/downloads/.

#### Demo

#### 1) Run python script from your local machine
       sagpalo-ltm2:awslogin sagpalo$ python3 create_repo.py 
#### 2) Enter a NAME for your new repository. Use naming convention "aws-tf-proj-[project_name]":
       ex. aws-tf-proj-test5
#### 3) Enter a list of space-separated BRANCHES where your code will be deployed. dev or ssdev is REQUIRED. i.e  dev ssdev uat qa prod ssprod :
       ex. dev prod
#### 4) Enter a list of space separated GITHUB USERNAMES who will serve as code owners: 
       ex. sherylla sreekantht05 sfdcit/scrum:

      {'repo_name': 'aws-tf-proj-test5', 'environments': ['dev', 'prod'], 'code_owners': ['sherylla', 'fcustodio', 'sreekantht05']}

#### 5) Upon Successful repository creation , you will receive:
       '"Repository Created Successfully!"
       
 ## How to use It : Backend
 
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

