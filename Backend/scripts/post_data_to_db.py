from urllib import response
from settings import *
import boto3
from generate_ids import create_country_ado_dict, generate_eight_digit_ids
import time 

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)


CountryAdoId = resource.Table(COUNTRY_ADO_ID_TABLE)
AdoAthelete = resource.Table(ADO_ATHLETE)

# if __name__ == "__main__":
    
#     for country in create_country_ado_dict():
#         try:
#             response = CountryAdoId.put_item(
#                 Item = country
#             )
#             time.sleep(1)
#         except Exception as e:
#             print(e.args)
            
#         print(response)

# if __name__ == "__main__":
    
#     response = CountryAdoId.delete_item(
#         Key = {
#             'Country':'Ireland',
#             'Id':2
#         }
#     )
    
#     print(response)

demo_countries = ['United States of America', 'United Kingdom' ,'Canada' , 'Ireland']

if __name__ == '__main__':
    for country in demo_countries:
        #ugh so risky but whatever
        ado = country + ' ' + 'ADO'
        for i in range(2):
            try:
                response = AdoAthelete.put_item(
                Item = {
                    'Ado': ado,
                    'AthleteId': str(generate_eight_digit_ids())
                    }
                )
                time.sleep(1)
                print(response)
            except Exception as e:
                print(e)
                
     





