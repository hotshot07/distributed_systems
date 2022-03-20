from settings import *
import boto3

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)


CountryAdoId = resource.Table(COUNTRY_ADO_ID_TABLE)


if __name__ == "__main__":
    response = CountryAdoId.put_item( 
                Item = {
                    'Country': 'Ireland',
                    'Id': 2
                }          
    )

    print(response)
    





