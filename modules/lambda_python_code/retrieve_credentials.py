import boto3
import json
import base64
from botocore.exceptions import ClientError
import os

def get_secret():
    secret_name = os.environ['secret_name']
    endpoint_url = "https://secretsmanager.us-west-2.amazonaws.com"
    region_name = "us-west-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        endpoint_url=endpoint_url
    )

    plaintext = ""
    print(secret_name)
    kms = session.client('kms')

    try:
        print("Retrieving the Encrypted secret...")
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        print("Encrypted secret retrieved")
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            
            print("Decrypting the Secret key")
            secret = json.loads(secret)
            plaintext = secret['token']
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        else:
            print("The request had invalid params:", e)

    return plaintext