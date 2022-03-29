import os
from decouple import config

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("REGION_NAME")

USER_PROFILE = "UserProfile"
AUTH_TABLE = "Auth"
COUNTRY_ADO = "CountryAdo"
