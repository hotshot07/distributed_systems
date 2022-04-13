import boto3
import botocore
from settings import *
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from flask import Response
import logging
from pprint import pprint
from werkzeug.security import generate_password_hash, check_password_hash

logger = logging.getLogger(__name__)

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)

client = boto3.client(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


UserProfile = resource.Table(USER_PROFILE)
AuthTable = resource.Table(AUTH_TABLE)
CountryAdo = resource.Table(COUNTRY_ADO)

# this function UPDATES an already existing account with the new information


def update_user_if_exists(**kwargs):
    try:
        response = UserProfile.update_item(
            Key={
                'Organization': kwargs['Organization'],
                'Id': kwargs['Id']
            },
            ConditionExpression="Organization = :o and Id = :i and AccountType = :t",
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
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            logger.error((f"Invalid request for {kwargs}: {e}"))
            return Response("Invalid parameters", 400)
        raise e

    logger.info(f"Updated profile of  user:{kwargs['Id']}")
    return Response("Profile updated", 200)


# check if id exists in database and its an orchestrator/admin account
def check_id(user_id, organization):
    try:
        response = UserProfile.query(
            KeyConditionExpression=Key('Id').eq(
                user_id) & Key('Organization').eq(organization)
        )

    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        return False
    else:
        if response['Count'] == 0:
            logger.error(
                f"User {user_id} does not exist or doesnt match organization {organization}")
            return False
        else:
            profile = response['Items'][0]
            if profile['AccountStatus'] == 'Active' and (profile['AccountType'] == 'Orchestrator' or profile['AccountType'] == 'Admin'):
                return True
            logger.error(f"User {user_id} is not an active orchestrator or admin")
            return False


def check_country(country):
    try:
        response = CountryAdo.query(
            KeyConditionExpression=Key('Country').eq(country)
        )

    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        logger.info(f"Country {country} does not exist")
        return False
    else:
        if response['Count'] == 0:
            return False
        return response['Items'][0]['Ado']


def create_inactive_account(item, account_type, organization):

    user_id = item['Id']

    password = item['Password']
    hashed_password = generate_password_hash(
        password, method='pbkdf2:sha256', salt_length=16)

    try:
        response = client.transact_write_items(
            TransactItems=[
                {
                    'Put': {
                        'TableName': AUTH_TABLE,
                        'Item': {
                            'userid': {
                                'S': str(user_id),
                            },
                            'hashed_password': {
                                'S': str(hashed_password)
                            }
                        }
                    }
                },
                {
                    'Put': {
                        'TableName': USER_PROFILE,
                        'Item': {
                            'Organization': {
                                'S': str(organization),
                            },
                            'Id': {
                                'S': str(user_id),
                            },
                            'AccountType': {
                                'S': str(account_type),
                            },
                            'AccountStatus': {
                                'S': 'Inactive'
                            },
                        },
                        'ConditionExpression': 'attribute_not_exists(Id)'
                    }
                }
            ]
        )
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        return Response("Error creating account", 400)
    else:
        return Response("Account created", 200)
