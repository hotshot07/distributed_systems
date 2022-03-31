from urllib import response
import boto3
import botocore
from boto3.dynamodb.conditions import Key
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
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)

AthleteTestTable = resource.Table(ATHELTE_TEST_TABLE)
AthleteAvailabilityTable = resource.Table(ATHLETE_AVAILABILITY_TABLE)
UserProfileTable = resource.Table(USER_PROFILE_TABLE)

def create_test_using_transaction(athlete_id, date, tester_id, orchestrator_id):
    import traceback
    try:
        athlete_test: AthleteTest = AthleteTest(
            athlete_id, date, tester_id, orchestrator_id)
        validate_item = athlete_test.validate_item()
        if not validate_item[0]:
            return validate_item[1], 400
        athlete_test_json = athlete_test.to_dynamo_json()
    except Exception as e:
        traceback.print_exc()
        return COULD_NOT_CREATE_TEST_MODEL, 400
    try:
        response = client.transact_write_items(
            TransactItems=[
                {
                    'Update': {
                        'TableName': ATHLETE_AVAILABILITY_TABLE,
                        'Key': {
                            'athlete_id': {'S': athlete_test.athlete.user_id},
                            'date': {'S': athlete_test.start_date},
                        },
                        'UpdateExpression': 'SET assigned_test=:t',
                        'ExpressionAttributeValues': {
                            ':t': {'BOOL': True},
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
        traceback.print_exc()
        return TRANSACTION_FAILED, 400
    return response, 200

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

def check_user_exists(user_id, user_role):
    response = UserProfileTable.query(IndexName="Id-index", KeyConditionExpression=Key('Id').eq(user_id))
    if response.get("Count", 0) == 1:
        return response.get("Items")[0].get("AccountType") == user_role, response.get("Items")[0].get("Organization")
    return False, None