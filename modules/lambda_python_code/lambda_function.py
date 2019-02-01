import json
import os
import api as f1
import base64
import retrieve_credentials as cred

def lambda_handler(event, context):
    #{"repo_name": "my_repo_name", "environments": ["sbx", "dev", "uat", "qa"], "code_owners": ["afraley", "fcustodio"]}
    branch_list = ['dev','qa','uat','prod','ssdev','ssprod','dr','soxprod','soxdr','vdassbx','itsssbx','lenelbadge','resvsbx1']
    #branch_list = os.environ['branch_list']
    #branch_list = json.loads(branch_list)
    token = cred.get_secret()
    pageNumber = 1
    numberOfRepos = 100
    dictGroupIdGroupName = {}
    listUserNames = []
    
    if "repo_name" in event and "environments" in event and "code_owners" in event:
        repo_name = event["repo_name"]
        accounts = event["environments"]
        users = event["code_owners"]
        ownerFileContent = '* '
        gitignoreFileContent = ''
        index = 0
        boolMakeSSDEVDefault = True
        
        for user in users:
            index = index + 1
            if index != len(users):
                ownerFileContent = ownerFileContent + '@'+ user + ' '
            else:
                ownerFileContent = ownerFileContent + '@'+ user
            
            if user.find("sfdcit/") < 0:
                r = f1.checkMembershipInOrganisation(user,token)
                if r.status_code == 204:
                    print(user , "is a member of sfdcit organisation")
                    listUserNames.append(user)
                else:
                    return "User membership not found"
            elif "sfdcit/" in user:
                teamId = f1.checkTeamExists(user,token)
                if teamId != -1:
                    print(user, " team exists in the organisation")
                    dictGroupIdGroupName[user] = teamId
                else:
                    return "Team not found"
            
        #getting the team Id for the scrum team            
        teamId = f1.checkTeamExists("scrum",token)
        if teamId != -1:
            dictGroupIdGroupName["scrum"] = teamId
        
        print (dictGroupIdGroupName)
        print (listUserNames)
        
        r = f1.createRepo(repo_name,token)
        response = json.loads(r.text)
        if r.status_code == 201:
            print("Repository created")
        elif r.status_code == 422 and response["errors"][0]["message"] == "name already exists on this account":
            return "Repository name already exists on this account"
        else:
            return "Error occured in the creation of the repo" + r.text
    
        #scaffolding - to create the directory and file structure - https://developer.github.com/v3/repos/contents/#create-a-file    
        f1.createNewFile(repo_name,token, ownerFileContent.encode('utf-8'), "master", "CODEOWNERS")
        gitignoreFileContent = f1.getgitIgnoreFileContent()
        f1.createNewFile(repo_name,token, gitignoreFileContent.encode('utf-8'), "master", ".gitignore")
        f1.createNewFile(repo_name,token, "#Placeholder".encode('utf-8'), "master", "modules/main/main.tf")
        readmeFileContent = f1.getreadmeFileContent()
        f1.createNewFile(repo_name,token, readmeFileContent.encode('utf-8'), "master", "README.md")
        
        #making the code owners as collaborators
        for username in listUserNames:
            f1.addUserAsCollaborator(username, repo_name, token)
            print (username + " added as collaborator")
        #updating team repositories
        for groupName in dictGroupIdGroupName:
            f1.addRepoForGroup(str(dictGroupIdGroupName[groupName]), repo_name, token)
            print (groupName + " added to the repository")
            
        for account in accounts:
            f1.createNewFile(repo_name,token, "#Placeholder".encode('utf-8'), "master", "envs/" + account + "-or/"+ account +"-or-vars.tf") 
        
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
        while numberOfRepos == 100:
            repos = f1.getAllRepos(token, str(pageNumber))
            repos = json.loads(repos.text)
            numberOfRepos = len(repos)
            print ('@ ' + str(numberOfRepos))
            pageNumber += 1

            for repo in repos:
                repo_name = repo["name"]
                print("Repo Name - ",repo_name)
                branches = f1.getAllBranches(repo_name,token)
                branches = json.loads(branches.text)
                for branch in branches:
                    branch_name = branch["name"]
                    print("    branch - ",branch_name)
                    if branch_name in branch_list:
                        isbranchProtected = f1.checkBranchProtection(repo_name,branch_name,token)
                        print("    branch protection status -",isbranchProtected)
                        if not isbranchProtected:
                            print("    Updating the Branch Protection...")
                            r = f1.setProtection(repo_name,token, branch_name)
                            if r.status_code != 200:
                                print("Branch Protection failed...")
                        print("    checking for isRepoBranchStausCheckEnabled ")
                        status = f1.isRepoBranchStausCheckEnable(repo_name,branch_name,token)
                        print("    isRepoBranchStausCheckEnabled returns -",status)
                        if status == False:
                            r = f1.setRepoBranchStausCheckEnable(repo_name,branch_name,token)
                            if r.status_code == 200:
                                print("Status check is now enabled...")
                            elif r.status_code == 422:
                                print("Status check already enabled response ...")
                        else:
                            print("Status check is already enabled...")

        return "Branch Protection Applied Successfully for the GitHub repos"
        #TODO: Ensure branch protection for existing repos
        #print("Ensuring branch protection for existing repositories...")