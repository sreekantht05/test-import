from botocore.vendored import requests
import json
import os
import base64

def createRepo(repo_name,token):
    print("Post call for creating a repository")
    url = "https://api.github.com/orgs/sfdcit/repos"
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    data = {}
    data["name"] = repo_name
    data["auto_init"] = "true"
    data["private"] = "false"
    data["gitignore_template"] = "nanoc"
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
    return r
