import json
import os
import api as f1
import base64
import retrieve_credentials as cred

def lambda_handler(event, context):
    #{"repo_name": "my_repo_name", "environments": ["sbx", "dev", "uat", "qa"], "code_owners": ["afraley", "fcustodio"]}
    
    token = cred.get_secret()
    
    if "repo_name" in event and "environments" in event and "code_owners" in event:
        repo_name = event["repo_name"]
        accounts = event["environments"]
        users = event["code_owners"]
        ownerFileContent = '* '
        index = 0
        boolMakeSSDEVDefault = True
        
        for user in users:
            index = index + 1
            if index != len(users):
                ownerFileContent = ownerFileContent + '@'+ user + ' '
            else:
                ownerFileContent = ownerFileContent + '@'+ user
            
            if user.find("sfdcit") < 0:
                r = f1.checkMembershipInOrganisation(user,token)
                if r.status_code == 204:
                    print(user , "is a member of sfdcit organisation")
                else:
                    return "User membership not found"
            elif "sfdcit" in user:
                isTeamExists = f1.checkTeamExists("consultants",token)
                if isTeamExists:
                    print(user, " team exists in the organisation")
                else:
                    return "Team not found"
        
        r = f1.createRepo(repo_name,token)
        response = json.loads(r.text)
        print(response)
        if r.status_code == 201:
            print("Repository created")
        elif r.status_code == 422 and response["errors"][0]["message"] == "name already exists on this account":
            return "Repository name already exists on this account"
        else:
            return "Error occured in the creation of the repo" + r.text
    
        #scaffolding - to create the directory and file structure - https://developer.github.com/v3/repos/contents/#create-a-file    
        f1.createNewFile(repo_name,token, ownerFileContent.encode('utf-8'), "master", "CODEOWNERS")
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
            if (account.lower() == 'dev'):
                boolMakeSSDEVDefault = False    
        f1.deleteMasterBranch(repo_name,token)    
    
        if boolMakeSSDEVDefault:
            f1.defaultBranch(repo_name,token,'ssdev')
        else:
            f1.defaultBranch(repo_name,token,'dev')
        
        #setting branch protection for all the environments
        for account in accounts:
            r = f1.setProtection(repo_name,token, account)
            print(r.status_code)
            print(r.json())
    
        returnResponse = {}
        returnResponse["Repository_Name"] = "sfdcit/"+repo_name+".git"
        returnResponse["Branches"] = accounts
        returnResponse["Code_Owners"] = users
        return returnResponse
    else:
        print("event doesnt contains repo_name or environments or code_owners details...")
        return "Invalid Parameters"
        #TODO: Ensure branch protection for existing repos
        #print("Ensuring branch protection for existing repositories...")