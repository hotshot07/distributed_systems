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
UserProfile = resource.Table(USER_PROFILE)

SET_OF_PARAMS_IN_USER_PROFILE = set({'Id', 'Organization', 'FirstName', 'LastName', 'Email', 'PhoneNumber', 'Country'})

def check_if_id_exists_in_table(**kwargs):
    try:
        response = AdoAthelete.query(
            KeyConditionExpression=Key('Ado').eq('{}'.format(kwargs['Ado'])) & Key('AthleteId').eq('{}'.format(kwargs['AthleteId']))
        )
        
        if response['Count'] == 0:
            return {'error': 'AthleteId or ADO does not exist in the database', 'status_code': 400}
        
    except ClientError as e:
        raise (e.response['Error']['Message'])
    else:
        return {'item': response['Items'], 'status_code': 200}



def create_user_if_not_exists(**kwargs):
    
    print(kwargs)
    
    try :
        response = UserProfile.query(
                KeyConditionExpression=Key('Organization').eq(f"{kwargs['Organization']}") & Key('Id').eq('{}'.format(kwargs['Id']))
        )
        if response['Count'] != 0:
            return {'error': 'User already exists', 'status_code': 409 }
    
    except ClientError as e:
        print(kwargs)
        raise (e.response['Error']['Message'])
    
    else:
        return insert_user_into_db(**kwargs)
    


def insert_user_into_db(**kwargs):
    
    try:
        response = UserProfile.put_item(
            Item = {
                'Organization': kwargs.get('Organization'),
                'Id': kwargs.get('Id'),
                'FirstName': kwargs.get('FirstName'),
                'LastName': kwargs.get('LastName'),
                'Email': kwargs.get('Email'),
                'Country': kwargs.get('Country'),
                'PhoneNumber': kwargs.get('PhoneNumber')
            }
        )
        
    except ClientError as e:
        raise (e.response['Error']['Message'])
    
    else:
        return {'item': response, 'status_code': 200}
    
        
        
    
    