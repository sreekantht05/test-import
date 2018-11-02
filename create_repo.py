import json
import boto3
from botocore.exceptions import ClientError

AWS_PROFILE = 'default'
REGION = 'us-west-2'
LAMBDA_FUNCTION_NAME = 'aws-tf-proj-template'


def get_user_input():
    inputs = {}
    inputs['repo_name'] = input('Enter the name of the repo, i.e. aws-tf-prof-myproject:\n')
    inputs['environments'] = input('Enter a list of space separated environment branches the repo should have. i.e. sbx dev uat qa prod:\n')
    inputs['code_owners'] = input('Enter a list of space separated github usernames to mark as a code owner:\n')

    #inputs['repo_name'] = 'shub_test_repo2'
    #inputs['environments'] = 'sbx ssprod'
    #inputs['code_owners'] = 'shubhashishraiSalesforce'

    inputs['environments'] = inputs['environments'].split(' ')
    inputs['code_owners'] = inputs['code_owners'].split(' ')

    return inputs

def trigger_lambda(inputs):

    session = boto3.session.Session(profile_name=AWS_PROFILE)
    client = session.client(
        service_name='lambda',
        region_name=REGION,
    )

    response = client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType='RequestResponse',
        # LogType='None'|'Tail',
        # ClientContext='string',
        Payload=json.dumps(inputs)
        # Qualifier='string'
    )

    for line in response['Payload'].iter_lines():
        print(line)

def main():
    """ Main """
    inputs = get_user_input()
    print (inputs)

    isDEVSSDEVBothAbsent = True
    for env in inputs['environments']:
        if env.upper() == 'DEV' or env.upper() == 'SSDEV':
            isDEVSSDEVBothAbsent = False 
            break

    if isDEVSSDEVBothAbsent:
        print ("Ensure at least DEV or SSDEV is included in the list of environments")
        return

    trigger_lambda(inputs)


if __name__ == "__main__":
    main()
