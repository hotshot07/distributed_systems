import boto3
import botocore
from settings import *
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from flask import Response
import logging
from pprint import pprint
from werkzeug.security import generate_password_hash, check_password_hash

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

        pprint(kwargs)

        response = UserProfile.update_item(
            Key={
                'Organization': kwargs['Organization'],
                'Id': kwargs['Id']
            },
            ConditionExpression="Organization = :o and Id = :i and AccountType = :t and AccountStatus = :ias",
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
            KeyConditionExpression=Key('Id').eq(
                user_id) & Key('Organization').eq(organization)
        )

    except ClientError as e:
        logging.error(e.response['Error']['Message'])
        return False
    else:
        if response['Count'] == 0:
            logging.error(
                f"User {user_id} does not exist or doesnt match organization {organization}")
            return False
        else:
            profile = response['Items'][0]
            if profile['AccountStatus'] == 'Active' and profile['AccountType'] == 'Orchestrator':
                return True
            logging.error(f"User {user_id} is not an active orchestrator")
            return False


def check_country(country):
    try:
        response = CountryAdo.query(
            KeyConditionExpression=Key('Country').eq(country)
        )

    except ClientError as e:
        logging.error(e.response['Error']['Message'])
        logging.info(f"Country {country} does not exist")
        return False
    else:
        if response['Count'] == 0:
            return False
        return True


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
        logging.error(e.response['Error']['Message'])
        return Response("Error creating account", 400)
    else:
        return Response("Account created", 200)
