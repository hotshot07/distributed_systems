from boto3.dynamodb.conditions import Attr
from decouple import config
import boto3

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME = config("REGION_NAME")


def connect():
    """
    Connection to AWS dynamodb
    :return: table of interest
    """
    dynamo_resource = boto3.resource(
        'dynamodb',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME
    )
    table = dynamo_resource.Table('AthleteTest')
    return table


def get_test_results(country):
    """
    Query table to fetch data
    :param country: country whose test results are asked
    :return: json response
    """
    response = connect().scan(
        IndexName='country-index',
        FilterExpression=Attr('country').eq(country)
    )
    print(response['Items'])
    if response['Items']:
        return response
    else:
        return f'No test results found for country {country}'
