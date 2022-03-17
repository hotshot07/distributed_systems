from boto3.dynamodb.conditions import Key
from decouple import config
import boto3

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME = config("REGION_NAME")


dynamo_resource = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)
table = dynamo_resource.Table('AthleteTest')


def get_test_results(country):
    response = table.query(
        KeyConditionExpression=Key('country').eq(country)
    )
    print(response['Items'])
    return response['Items']
