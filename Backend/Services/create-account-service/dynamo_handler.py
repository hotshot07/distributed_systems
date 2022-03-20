import boto3, botocore
from settings import *
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)


CountryAdoId = resource.Table(COUNTRY_ADO_ID_TABLE)
AdoAthelete = resource.Table(ADO_ATHLETE)

def check_if_id_exists_in_table(**kwargs):
    try:
        response = AdoAthelete.query(
            KeyConditionExpression=Key('Ado').eq('{}'.format(kwargs['Ado'])) & Key('AthleteId').eq('{}'.format(kwargs['AthleteId']))
        )
        
        if response['Count'] == 0:
            return {'error': 'AthleteId or ADO does not exist in the database', 'status_code': 400}
        
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return {'item': response['Items'], 'status_code': 200}
    