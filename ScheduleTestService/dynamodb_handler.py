import boto3, botocore
from settings import *
from models import *

client = boto3.client(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)
resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)

AthleteTestTable = resource.Table(ATHELTE_TEST_TABLE)
AthleteAvailabilityTable = resource.Table(ATHLETE_AVAILABILITY_TABLE)

def create_test(athlete_id, date, tester_id, orchestrator_id):
    try:
        athlete_test : AthleteTest = AthleteTest(athlete_id, date, tester_id, orchestrator_id)
        athlete_test_json = athlete_test.as_json()
    except Exception as e:
        return e.args, ITEM_PARAMETERS_INVALID
    # TODO Create Transaction here
    #   1. Update availability item to say that it has been assigned
    #   2. Create athlete test item
    #   ? Might need to use a form of optimistic locking
    try:
        response = AthleteTestTable.put_item(
            Item = athlete_test_json,
            ConditionExpression='attribute_not_exists(athlete_id) AND attribute_not_exists(test_datetime)'
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return athlete_test_json, ITEM_COULD_NOT_BE_ADDED
        raise e
    return athlete_test_json, response

def update_test_result(tester_id, test_datetime, test_result):
    try:
        response = AthleteTestTable.update_item(
            Key = {
                'tester_id': tester_id,
                'test_datetime': test_datetime
            },
            UpdateExpression='SET #res.#res = :val',
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