import boto3, botocore
from settings import *
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from flask import Response
import logging
from pprint import pprint 

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)

UserProfile = resource.Table(USER_PROFILE)

#this function UPDATES an already existing account with the new information
def create_user_if_not_exists(**kwargs):
    try:
        
        pprint(kwargs)
        
        response = UserProfile.update_item(
            Key={
                'Organization': kwargs['Organization'],
                'Id': kwargs['Id']
            },
            ConditionExpression = "Organization = :o and Id = :i and AccountType = :t and AccountStatus = :ias",
            UpdateExpression="set FirstName = :fn, LastName = :ln, Email = :e, PhoneNumber = :pn, Country = :c, AccountStatus = :s",
            ExpressionAttributeValues={
                ':o': kwargs['Organization'],
                ':i': kwargs['Id'],
                ':fn': kwargs['FirstName'],
                ':ln': kwargs['LastName'],
                ':e': kwargs['Email'],
                ':pn': kwargs['PhoneNumber'],
                ':c': kwargs['Country'],
                ':t': kwargs['AccountType'],
                ':s': 'Active',
                ':ias': 'Inactive'
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            logging.error((f"Invalid request for {kwargs}: {e}"))
            return Response("Invalid parameters", 400)
        raise e
    
    logging.info(f"Created user {kwargs['Id']}")
    return Response("Account created", 200)


# check if id exists in database and its an orchestrator
def check_id(user_id, organization):
    try:
        response = UserProfile.query(
            KeyConditionExpression=Key('Id').eq(user_id) & Key('Organization').eq(organization)
        )
        
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
        return False
    else:
        if response['Count'] == 0:
            logging.error(f"User {user_id} does not exist")
            return False
        else:
            profile = response['Items'][0]
            if profile['AccountStatus'] == 'Active' and profile['AccountType'] == 'Orchestrator':
                return True
            logging.error(f"User {user_id} is not an active orchestrator")
            return False


#this function CREATES a new account 
# def create_inactive_athelete_accounts(list_of_accounts, type_of_account):
    
#     # list of accoutns is a list of dictionaries with userid/pwd combo 
    
#     for user_item in list_of_accounts: