import boto3, botocore
from decouple import config

AWS_ACCESS_KEY_ID     = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME           = config("REGION_NAME")

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

#TODO
def create_test(availability_id, tester):
    try:
        response = AthleteTestTable.put_item(
            Item = {
                'availability_id': "1",
                'country': "Ireland",
                'info': "test",
            },
            ConditionExpression='attribute_not_exists(availability_id) AND attribute_not_exists(country)'
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return "Item already exists"
        raise e
    return response