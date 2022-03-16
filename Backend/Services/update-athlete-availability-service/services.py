import re
import boto3
from botocore.exceptions import ClientError

import settings

#TODO: Insert Correct times
#TODO: More error handling


#Create Resource
def connect():
    dynamo_resource = boto3.resource(
        'dynamodb',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.REGION_NAME
        )
    return dynamo_resource


#PUT
def put_item(country, athlete_id, dynamo):
    table = dynamo.Table(settings.ATHLETE_AVAILABILITY_TABLE)
    try:
        response = table.put_item(
            Item={
                'athlete_country': country,
                'athlete_id': athlete_id,
                'availability': {} #initialise empty
            },
            ConditionExpression='attribute_not_exists(athlete_country) AND attribute_not_exists(athlete_id)'
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            #handle this
            print(e.response['Error']['Message'])
    else:
        return response['Item']


#UPDATE
def update_item(country, athlete_id, item, dynamo):
    table = dynamo.Table(settings.ATHLETE_AVAILABILITY_TABLE)

    try:
        response = table.update_item(
            Key={
                'athlete_country': country,
                'athlete_id': athlete_id
            },
            UpdateExpression='set availability.{}=:loc'.format(item['date']),
            ExpressionAttributeValues={
                ':loc' : item['location']
            },
            ReturnValues="ALL_NEW"
        )
    except ClientError as e:
        print("ERR:", e.response['Error']['Message'])
    else:
        return response


#update availability
def update_availability(country, athlete_id, availability):
    dynamo = connect()
    for item in availability:
        resp = update_item(country, athlete_id, item, dynamo=dynamo)
        if resp == None:
            break
    if resp:
        return "Updated Successfully"
    else:
        return None

#initialise availability
def initialise_availability(country, athlete_id):
    dynamo = connect()
    resp = put_item(country, athlete_id, dynamo)
    if resp:
        return "Initialised Successfully"
    else:
        return None

