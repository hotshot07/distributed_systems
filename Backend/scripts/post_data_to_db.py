from urllib import response
from settings import *
import boto3
from generate_ids import create_country_ado_dict, generate_ten_digit_ids
import time

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


CountryAdo = resource.Table("CountryAdo")
UserProfile = resource.Table(USER_PROFILE)

# if __name__ == "__main__":

#     for country in create_country_ado_dict():
#         try:
#             response = CountryAdo.put_item(
#                 Item = country
#             )
#             time.sleep(1)
#         except Exception as e:
#             print(e.args)

#         print(response)


# def auth_function(userid,pwd):

#     # check if creds exist in dynamo

#     userid_pwd = {
#         'userid': userid,
#         'pwd': pwd
#     }

#     # db has userid, pwd, hulib (has user logged in before)

#     response = CountryAdoId.query(
#                 Item = userid_pwd
#             )

# if item exists, check if hulib is true
# if false, when returning return "inital login"

# update hublib to true

# return 'OK', 200


# if __name__ == "__main__":

#     response = CountryAdoId.delete_item(
#         Key = {
#             'Country':'Ireland',
#             'Id':2
#         }
#     )

#     print(response)

# demo_countries = ['United States of America', 'United Kingdom' ,'Canada' , 'Ireland']
# athlete_ids = [generate_ten_digit_ids() for i in range(len(demo_countries))]

# if __name__ == '__main__':
#     for country, ids in zip(demo_countries, athlete_ids):
#         item_dict = {
#             'Organization': 'WADA',
#             'Id': str(ids),
#             'AccountType': 'WADA',
#             'AccountStatus': 'Inactive'
#         }

#         response = UserProfile.put_item(
#                 Item = item_dict
#             )

#         print(response)

#         time.sleep(1)
