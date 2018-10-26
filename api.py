from botocore.vendored import requests
import json
import os

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
