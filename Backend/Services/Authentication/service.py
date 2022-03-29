import boto3
from settings import (
    AUTH,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    REGION_NAME,
    USER_PROFILE,
)

resource = boto3.resource(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


AuthTable = resource.Table(AUTH)
UserProfileTable = resource.Table(USER_PROFILE)
