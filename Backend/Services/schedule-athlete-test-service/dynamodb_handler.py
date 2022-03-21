import boto3
import botocore
from settings import *
from models import *

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)

client = boto3.client(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)

AthleteTestTable = resource.Table(ATHELTE_TEST_TABLE)
AthleteAvailabilityTable = resource.Table(ATHLETE_AVAILABILITY_TABLE)


def create_test_using_transaction(athlete_id, date, tester_id, orchestrator_id):
    try:
        athlete_test: AthleteTest = AthleteTest(
            athlete_id, date, tester_id, orchestrator_id)
        athlete_test_json = athlete_test.to_dynamo_json()
    except Exception as e:
        return e.args, ITEM_PARAMETERS_INVALID
    # TODO ? Might need to use a form of optimistic locking
    try:
        response = client.transact_write_items(
            TransactItems=[
                {
                    'Update': {
                        'TableName': ATHLETE_AVAILABILITY_TABLE,
                        'Key': {
                            'athlete_id': {'S':athlete_test.athlete.user_id},
                            'date': {'S':athlete_test.start_date},
                        },
                        'UpdateExpression': 'SET assigned_test=:t',
                        'ExpressionAttributeValues': {
                            ':t': {'BOOL':True},
                        },
                        'ConditionExpression': 'attribute_not_exists(assigned_test)'
                    }
                },
                {
                    'Put': {
                        'TableName': ATHELTE_TEST_TABLE,
                        'Item': athlete_test_json,
                        'ConditionExpression': 'attribute_not_exists(athlete_id) AND attribute_not_exists(tester_id) AND attribute_not_exists(test_datetime)'
                    }
                }
            ]
        )
    except Exception as e:
        return e.args, ITEM_PARAMETERS_INVALID
    return athlete_test_json, response

def update_test_result(tester_id, test_datetime, test_result):
    try:
        response = AthleteTestTable.update_item(
            Key={
                'tester_id': tester_id,
                'test_datetime': test_datetime
            },
            UpdateExpression='SET #res = :val',
            ExpressionAttributeValues={
                ":val": test_result
            },
            ExpressionAttributeNames={
                "#res": "result",
            }
        )
    except Exception as e:
        return e.args, 404
    else:
        return response, 200

