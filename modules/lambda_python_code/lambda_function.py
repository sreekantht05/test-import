import json
import os
import api as f1
import base64
import retrieve_credentials as cred

def lambda_handler(event, context):
    #{"repo_name": "my_repo_name", "environments": ["sbx", "dev", "uat", "qa"], "code_owners": ["afraley", "fcustodio"]}
    
    repo_name = event["repo_name"]   #os.environ['repo_name']
    accounts = event["environments"]    #os.environ['accounts']
    users = event["code_owners"]      #["shubhashishraiSalesforce"]
    ownerFileContent = ''
    index = 0
    boolMakeSSDEVDefault = True
    
    token = cred.get_secret()
    
    for user in users:
        index = index + 1
        if index != len(users):
            ownerFileContent = ownerFileContent + user + ','
        else:
            ownerFileContent = ownerFileContent + user
        r = f1.checkUserExists(user,token)
        
        if r.status_code == 200:
            print("User exists")
        else:
            return "User Not exists"
    
    print("Creating a repository")
    
    r = f1.createRepo(repo_name,token)
    print(r.status_code)
    
    response = json.loads(r.text)
    print(response)
    if r.status_code == 201:
        print("Repository created")
        #return "Repository Created"
    elif r.status_code == 422 and response["errors"][0]["message"] == "name already exists on this account":
        return "name already exists on this account"
    else:
        return "Error occured in the creation of the repo" + r.text

    #scaffolding - to create the directory and file structure - https://developer.github.com/v3/repos/contents/#create-a-file    
    f1.createNewFile(repo_name,token, ownerFileContent.encode('utf-8'), "master", ".owners")
    #f1.createNewFile(repo_name,token, "#Placeholder".encode('utf-8'), "master", ".gitignore")
    f1.createNewFile(repo_name,token, "#Placeholder".encode('utf-8'), "master", "modules/main/main.tf")
    
    for account in accounts:
        f1.createNewFile(repo_name,token, "#Placeholder".encode('utf-8'), "master", "envs/" + account + "/main.tf")  
    
    r = f1.getMasterSHA(repo_name,token)
    response = json.loads(r.text)
    print(response)
    
    shaMaster = response["object"]["sha"]
    print(shaMaster)
    
    for account in accounts:
        f1.createBranch(repo_name,token, account, shaMaster)
        if (account.upper() == 'DEV'):
            boolMakeSSDEVDefault = False    
    f1.deleteMasterBranch(repo_name,token)    

    if boolMakeSSDEVDefault:
        f1.defaultBranch(repo_name,token,'ssdev')
    else:
        f1.defaultBranch(repo_name,token,'dev')
        
    for account in accounts:
        r = f1.setProtection(repo_name,token, account)
        print(r.status_code)
        print(r.json())

    #To Dos:
    #branch protection - https://developer.github.com/v3/repos/branches/#update-branch-protection
    #lambda job to run periodically/daily to ensure the branch protection rules are intact. - https://developer.github.com/v3/repos/branches/#update-branch-protection
    
    return "Repository created successfully!"
