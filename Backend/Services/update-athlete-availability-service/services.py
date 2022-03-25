import boto3
from botocore.exceptions import ClientError

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

    try:
        response = table.put_item(
            Item={
                'athlete_id': availability.athlete_id,
                'date': availability.date,
                'available_time': availability.available_time,
                'location_address': availability.location_address,
                'location_country': availability.location_country
            }
        )
        return response

    except ClientError as e:
        raise e


#update availability
def update_availability(availability):
    dynamo = connect()
    resp = put_item(availability, dynamo=dynamo)
    return resp