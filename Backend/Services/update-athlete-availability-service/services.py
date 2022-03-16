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
def update_item(athlete_id, date_time, location, country, dynamo):
    table = dynamo.Table(ATHLETE_AVAILABILITY_TABLE)

    date_time = datetime.datetime.fromisoformat(date_time)

    date_attribute = date_time.date().isoformat()
    date_time_attribute = date_time.isoformat()

    try:
        response = table.update_item(
            Key={
                'athlete_id': athlete_id,
                'date': date_attribute,
            },
            UpdateExpression='set date_time = :dt, location_address = :loc, location_country = :c',
            ExpressionAttributeValues={
                    ':dt' : date_time_attribute,
                    ':loc': location,
                    ':c': country
            },
            ReturnValues="ALL_NEW"
        )
    except ClientError as e:
        print("ERR:", e.response['Error']['Message'])
    else:
        return response


#update availability
def update_availability(athlete_id, date_time, location, country):
    dynamo = connect()
    resp = update_item(athlete_id, date_time, location, country, dynamo=dynamo)
    if resp:
        return UPDATE_SUCCESS
    else:
        return None