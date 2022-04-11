from boto3.dynamodb.conditions import Key
import boto3
from settings import (
    ATHLETE_TEST_TABLE,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    REGION_NAME,
)


def connect():
    """
    Connection to AWS dynamodb
    :return: table of interest
    """
    dynamo_resource = boto3.resource(
        "dynamodb",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME,
    )
    table = dynamo_resource.Table(ATHLETE_TEST_TABLE)
    return table


def get_test_results(country):
    """
    Query table to fetch data
    :param country: country whose test results are asked
    :return: json response
    """
    index = 1
    data_to_return = {}

    response = connect().query(
        IndexName="country-index", KeyConditionExpression=Key("country").eq(country)
    )
    queryCount = 1

    items = response['Items']
    for item in items:
        data_to_return[index] = item
        index += 1
        
    queryCount += 1

    while 'LastEvaluatedKey' in response:
        key = response['LastEvaluatedKey']
        response = connect().query(
        IndexName="country-index", KeyConditionExpression=Key("country").eq(country), ExclusiveStartKey=key
    )
        items = response['Items']
        for item in items:
            data_to_return[index] = item
            index += 1
        
        queryCount += 1

    return (
        data_to_return
        if data_to_return
        else f"No test results found for country {country}"
    )
    
