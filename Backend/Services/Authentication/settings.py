import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("REGION_NAME")

USER_PROFILE = "UserProfile"
AUTH = "Auth"


USER_DOES_NOT_EXIST = "User does not exist"
INVALID_TOKEN = "Token is Invalid"
MISSING_TOKEN = "Token is missing"
USER_AUTHENTICATED = "Token returned.User authenticated"
COULD_NOT_VERIFY = "Could not verify"
TOKEN_EXPIRY_MINUTES = 30
