import datetime
import boto3
from botocore.exceptions import ClientError

from settings import *

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


#UPDATE
def update_item(availability, dynamo):
    table = dynamo.Table(ATHLETE_AVAILABILITY_TABLE)

    try:
        response = table.update_item(
            Key={
                'athlete_id': availability.athlete_id,
                'date': availability.date,
            },
            UpdateExpression='set available_time = :t, location_address = :loc, location_country = :c',
            ExpressionAttributeValues={
                    ':t' : availability.available_time,
                    ':loc': availability.location_address,
                    ':c': availability.location_country
            },
            ReturnValues="ALL_NEW"
        )
    except ClientError as e:
        print("ERR:", e.response['Error']['Message'])
    else:
        return response


#update availability
def update_availability(availability):
    dynamo = connect()
    resp = update_item(availability, dynamo=dynamo)
    return resp