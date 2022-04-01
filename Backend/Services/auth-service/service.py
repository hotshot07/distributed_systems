import boto3
from boto3.dynamodb.conditions import Key

from settings import (
    AUTH,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    REGION_NAME,
    USER_PROFILE,
)

resource = boto3.resource(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


AuthTable = resource.Table(AUTH)
UserProfileTable = resource.Table(USER_PROFILE)


def query_user_profile_table_email(username):
    return UserProfileTable.query(
        IndexName="Email-index", KeyConditionExpression=Key("Email").eq(username)
    )


def query_user_profile_table_id(user_id):
    return UserProfileTable.query(
        IndexName="Id-index", KeyConditionExpression=Key("Id").eq(user_id)
    )


def query_auth_table(user_id):
    return AuthTable.query(
        IndexName="userid-index", KeyConditionExpression=Key("userid").eq(user_id)
    )
