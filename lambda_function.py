import json
import os
import api as f1

def lambda_handler(event, context):
    #{"repo_name": "my_repo_name", "environments": ["sbx", "dev", "uat", "qa"], "code_owners": ["afraley", "fcustodio"]}
    repo_name = event["repo_name"]   #os.environ['repo_name']
    accounts = event["environments"]    #os.environ['accounts']
    users = event["code_owners"]      #["shubhashishraiSalesforce"]
    
    for user in users:
        print(user)
        r = f1.checkUserExists(user)
        
        if r.status_code == 200:
            print("User exists")
        else:
            return "User Not exists"
    
    print("Creating a repositoy")
    
    r = f1.createRepo(repo_name)
    print(r.status_code)
    
    response = json.loads(r.text)
    print(response)
    if r.status_code == 201:
        print("Repository created")
        return "Repository Created"
    elif r.status_code == 422 and response["errors"][0]["message"] == "name already exists on this account":
        return "name already exists on this account"
