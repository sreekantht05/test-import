#!/bin/bash

repo_name=$1
accounts='sbx dev qa uat prod ssdev ssprod'

if [ "$repo_name" = "" ]; then
   echo "Enter repository name: "
   read repo_name
fi

if [ "$repo_name" = "" ]; then
   echo "No repository name provided. Run the script again and provide a repository name"
   exit 1
fi

username=`git config github.user`
if [ "$username" = "" ]; then
   echo "Could not find username, run 'git config --global github.user <username>'"
   invalid_credentials=1
fi

token=`git config github.token`
if [ "$token" = "" ]; then
   echo "Could not find token, run 'git config --global github.token <token>'"
   invalid_credentials=1
fi

if [ "$invalid_credentials" == "1" ]; then
   return 1
fi

mkdir $repo_name
cd $repo_name
echo -n "Creating Github repository '$repo_name' ..."
curl -u "$username:$token" https://api.github.com/orgs/sfdcit/repos -d '{"name":"'$repo_name'"}' > /dev/null 2>&1
echo " done."

echo -n "Setting up your new repo..."
echo "# This serves as the user documentation for your code" >> README.md
echo "# TF Owners" >> .owners
echo "#  Local .terraform directories
**/.terraform/*

# .tfstate files
*.tfstate
*.tfstate.*

# .tfvars files
*.tfvars" >> .gitignore

for account in $accounts
do
   mkdir -p envs/$account/ && echo " # main.tf" >> envs/$account/main.tf
done

mkdir -p modules/main/ && echo " # main.tf" >> modules/main/main.tf

git init
git add .
git commit -m "first commit"
git branch -m dev

echo -n "Pushing local code to remote ..."
git remote add origin https://github.com/sfdcit/$repo_name.git > /dev/null 2>&1
git push -u origin dev > /dev/null 2>&1
echo " done."

