/*provider "aws" {
  region  = "us-west-2"
  profile = "dev"
}*/

module "main" {
  source = "../../modules/main"
}
