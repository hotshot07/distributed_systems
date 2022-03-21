import boto3, botocore
from settings import *
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from flask import Response

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)


CountryAdoId = resource.Table(COUNTRY_ADO_ID_TABLE)
UserProfile = resource.Table(USER_PROFILE)

SET_OF_PARAMS_IN_USER_PROFILE = set({'Id', 'Organization', 'FirstName', 'LastName', 'Email', 'PhoneNumber', 'Country'})

def create_user_if_not_exists(**kwargs):
    try:
        response = UserProfile.update_item(
            Key={
                'Organization': kwargs['Organization'],
                'Id': kwargs['Id']
            },
            ConditionExpression = "Organization = :o and Id = :i and AccountType = :t",
            UpdateExpression="set FirstName = :fn, LastName = :ln, Email = :e, PhoneNumber = :pn, Country = :c, AccountStatus = :s, AccountType = :t",
            ExpressionAttributeValues={
                ':o': kwargs['Organization'],
                ':i': kwargs['Id'],
                ':fn': kwargs['FirstName'],
                ':ln': kwargs['LastName'],
                ':e': kwargs['Email'],
                ':pn': kwargs['PhoneNumber'],
                ':c': kwargs['Country'],
                ':t': kwargs['AccountType'],
                ':s': 'Active'
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return Response("Invalid parameters", 400)
        raise e
    
    return Response("Account created", 200)
            
    
        
        
    
    