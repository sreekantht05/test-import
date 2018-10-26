from botocore.vendored import requests
import json
import os
import base64

def createRepo(repo_name):
    print("Post call for creating a repo")
    token = os.environ['token']
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
    print(headers)
    r = requests.post(url, data=data, headers=headers)
    print(r)
    return r

def checkUserExists(user):
    url = "https://api.github.com/users/"+user
    headers = {}
    token = os.environ['token']
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    r = requests.get(url,headers=headers)
    return r

def checkRepoExists(repo_name):
    url = "https://api.github.com/orgs/sfdcit/repos/"+repo_name
    token = os.environ['token']
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    r = requests.get(url,headers=headers)
    return r

def createNewFile(repo_name, content, branch, file_path):
    print("Put calls for creating new file  s")
    url = "https://api.github.com/repos/sfdcit/" + repo_name + "/contents/" + file_path #test6.txt
    token = os.environ['token']
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

def getMasterSHA(repo_name):
    url = "https://api.github.com/repos/sfdcit/" + repo_name + "/git/refs/heads/master"
    print (url)
    headers = {}
    token = os.environ['token']
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    r = requests.get(url,headers=headers)
    return r

def createBranch(repo_name, branch_name, sha):
    print("Post call for creating a branch")
    token = os.environ['token']
    url = "https://api.github.com/repos/sfdcit/" + repo_name + "/git/refs"
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    data = {}
    data["ref"] = "refs/heads/" + branch_name
    data["sha"] = sha
    data = json.dumps(data)
    r = requests.post(url, data=data, headers=headers)
    print(r)
    return r

def deleteMasterBranch(repo_name):
    token = os.environ['token']
    url = "https://api.github.com/repos/sfdcit/" + repo_name + "/git/refs/heads/master"
    headers = {}
    headers["Content-Type"]="application/json"
    headers["Authorization"] = "token "+token
    r = requests.delete(url, headers=headers)
    print(r)
    return r  
