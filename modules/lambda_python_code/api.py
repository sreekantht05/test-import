from botocore.vendored import requests
import json
import os
import base64
import hcl

def createRepo(repo_name,token):
    print("Post call for creating a repository")
    url = "https://api.github.com/orgs/sfdcit/repos"
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    data = {}
    data["name"] = repo_name
    #data["auto_init"] = "false" - commented to not default with a readme
    data["private"] = "true"
    data = json.dumps(data)
    r = requests.post(url, data=data, headers=headers)
    return r

def checkMembershipInOrganisation(user,token):
    url = "https://api.github.com/orgs/sfdcit/members/"+user
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    r = requests.get(url,headers=headers)
    return r

def createNewFile(repo_name, token, content, branch, file_path):
    print("Put calls for creating new file - ",file_path)
    url = "https://api.github.com/repos/sfdcit/" + repo_name + "/contents/" + file_path
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    data = {}
    data["message"] = "git scaffolding"
    data["content"] = base64.b64encode(content).decode('utf-8')
    data["branch"] = branch
    data = json.dumps(data)
    r = requests.put(url, data=data, headers=headers)
    return r

def getMasterSHA(repo_name,token):
    url = "https://api.github.com/repos/sfdcit/" + repo_name + "/git/refs/heads/master"
    print (url)
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    r = requests.get(url,headers=headers)
    return r

def createBranch(repo_name, token, branch_name, sha):
    print("Post call for creating a branch")
    url = "https://api.github.com/repos/sfdcit/" + repo_name + "/git/refs"
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    data = {}
    data["ref"] = "refs/heads/" + branch_name
    data["sha"] = sha
    data = json.dumps(data)
    r = requests.post(url, data=data, headers=headers) 
    return r

def deleteMasterBranch(repo_name,token):
    url = "https://api.github.com/repos/sfdcit/" + repo_name + "/git/refs/heads/master"
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    r = requests.delete(url, headers=headers)  
    return r  

def defaultBranch(repo_name, token, branch_name):
    url = "https://api.github.com/repos/sfdcit/" + repo_name
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    data = {}
    data["name"] = repo_name
    data["default_branch"] = branch_name
    data = json.dumps(data)
    r = requests.patch(url, data=data, headers=headers)
    return r  

def setProtection(repo_name,token,branch_name):
    url = "https://api.github.com/repos/sfdcit/" + repo_name + "/branches/" + branch_name + "/protection"
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    data = {
        "restrictions": None,
        "required_status_checks": {
            "strict": True,
            "contexts": []
        },
        "enforce_admins": False,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": True
        }
    }
    r = requests.put(url, json=data, headers=headers)
    print("Branch protection updation status code " + str(r.status_code))
    return r

def checkRepoExists(repo_name,token):
    url = "https://api.github.com/orgs/sfdcit/repos/"+repo_name
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    r = requests.get(url,headers=headers)
    return r

def checkTeamExists(team_name,token):
    url = "https://api.github.com/orgs/sfdcit/teams"
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    r = requests.get(url,headers=headers)
    teams = json.loads(r.text)
    teamId = -1
    for team in teams:
        if team_name.replace("sfdcit/","") == team["name"]:
            teamId = team ["id"]
            break
    return teamId

def getgitIgnoreFileContent():
    file_content = open("pythonTerraform.gitignore", 'r').read()
    return file_content

def getreadmeFileContent():
    file_content = open("readme.template", 'r').read()
    return file_content

def getAllRepos(token, pageNumber):
    url = "https://api.github.com/orgs/sfdcit/repos?per_page=100&page=" + pageNumber
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    r = requests.get(url, headers=headers)
    return r

def getAllBranches(repo_name,token):
    url = "https://api.github.com/repos/sfdcit/"+repo_name+"/branches"
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    r = requests.get(url, headers=headers)
    return r

def checkBranchProtection(repo_name,branch_name,token):
    url = "https://api.github.com/repos/sfdcit/"+repo_name+"/branches/"+branch_name
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    r = requests.get(url, headers=headers)
    branch_details = json.loads(r.text)
    return branch_details["protected"]
    
def addUserAsCollaborator(username, repo_name, token):
    url = "https://api.github.com/repos/sfdcit/" + repo_name + "/collaborators/" + username
    headers = {}
    headers["Authorization"] = "token "+token
    r = requests.put(url, headers=headers)
    print("user as collaborator status code " + str(r.status_code))
    
def addRepoForGroup(groupId, repo_name, token):
    url = "https://api.github.com/teams/" + groupId + "/repos/sfdcit/" + repo_name
    headers = {}
    headers["Authorization"] = "token "+token
    headers["Accept"] = "application/vnd.github.hellcat-preview+json"
    headers["Content-Type"] = "application/json"
    data = {}
    data["permission"] = "push"
    data = json.dumps(data)
    r = requests.put(url, data=data, headers=headers)
    print("group added status code " + str(r.status_code))
    
def setRepoBranchStausCheckEnable(repo_name,branch_name,token):
    setProtection(repo_name,token,branch_name)
    url = "https://api.github.com/repos/sfdcit/" + repo_name + "/branches/" + branch_name + "/protection/required_status_checks/contexts"
    headers = {}
    headers["Authorization"] = "token "+token
    headers["Content-Type"] = "application/json"
    context_name = "AWS CodeBuild us-west-2 ("+repo_name+"-tfplan)"
    data = [context_name]
    data = json.dumps(data)
    r = requests.post(url, data=data, headers=headers)
    return r

def isRepoBranchStausCheckEnable(repo_name,branch_name,token):
    url = "https://api.github.com/repos/sfdcit/" + repo_name + "/branches/" + branch_name + "/protection/required_status_checks/contexts"
    headers = {}
    headers["Authorization"] = "token "+token
    headers["Content-Type"] = "application/json"
    context_name = "AWS CodeBuild us-west-2 ("+repo_name+"-tfplan)"

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        response = json.loads(r.text)
        print(response)
        if len(response) >0:
            if context_name in response:
                return True
        else:
            return False
    return False

def get_pipeline_file_content(token, repo_name, branch_name):
    url = "https://api.github.com/repos/sfdcit/"+ repo_name +"/contents/envs/" + branch_name + "/" + branch_name + "-vars.tf?ref=" + branch_name
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        response = json.loads(r.text)
        content = response["content"]
        content = base64.b64decode(content)
        print(content)
    return content

def get_module_list(content):
    try:
        data = hcl.loads(content)
        if "module" in data:
            module = data["module"]
            return module
    except ValueError as e:
        print(e)