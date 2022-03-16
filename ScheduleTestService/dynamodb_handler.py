import boto3, botocore
from constants import *
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

AthleteTestTable = resource.Table('AthleteTest')

def create_test(availability_id, tester_id, orchestrator_id):
    athlete_test : AthleteTest = AthleteTest(availability_id, tester_id, orchestrator_id)
    athlete_test_json = athlete_test.as_json()
    # TODO Create Transaction here, !!!check tester is not assigned anywhere else at the time!!!
    try:
        response = AthleteTestTable.put_item(
            Item = athlete_test_json,
            ConditionExpression='attribute_not_exists(test_id) AND attribute_not_exists(country)'
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return athlete_test_json, ITEM_ALREADY_EXISTS
        raise e
    return athlete_test_json, response

def update_test_result(test_id, country, test_result):
    response = AthleteTestTable.update_item(
        Key = {
            'test_id': test_id,
            'country': country
        },
        UpdateExpression='SET #res.#res = :val',
        ExpressionAttributeValues={
            ":val": test_result
        },
        ExpressionAttributeNames={
            "#res": "result",
        }
    )
    return response


#print(update_test_result("2", "Ireland", "POSTI2VE"))
#print(create_test("2", "3", "4"))