import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

from settings import *
from models import AthleteAvailability

#TODO: More error handling

#Create Resource
def connect():
    dynamo_resource = boto3.resource(
        'dynamodb',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME
        )
    return dynamo_resource


def put_item(availability: AthleteAvailability, dynamo):
    table = dynamo.Table(ATHLETE_AVAILABILITY_TABLE)
    availability_item = availability.__dict__
    try:
        response = table.put_item(
            Item=availability_item
        )
        return response

    except ClientError as e:
        raise e


def create_availability(availability):
    dynamo = connect()
    resp = put_item(availability, dynamo=dynamo)
    return resp


def get_items(athlete_id: str, dynamo):
    table = dynamo.Table(ATHLETE_AVAILABILITY_TABLE)
    try:
        response = table.query(
            KeyConditionExpression=Key('athlete_id').eq(athlete_id)
        )
        if response['Items']:
            return response['Items']
        else:
            return []

    except ClientError as e:
        raise e


def get_availability(availability: int):
    dynamo = connect()
    resp = get_items(availability, dynamo=dynamo)
    return resp