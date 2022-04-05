import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("REGION_NAME")

USER_PROFILE = "UserProfile"
AUTH = "Auth"

SECRET_KEYS = {
    "Athlete": "thisisthesecretkeyAthlete",
    "Tester": "thisisthesecretkeyTester",
    "Orchestrator": "thisisthesecretkeyOrchestrator",
    "WADA": "thisisthesecretkeyWADA",
    "Admin": "thisisthesecretkeyAdmin"
}

USER_DOES_NOT_EXIST = "User does not exist"
INVALID_TOKEN = "Token is Invalid"
MISSING_TOKEN = "Token is missing"
USER_AUTHENTICATED = "Token returned. User is authenticated"
COULD_NOT_VERIFY = "Could not verify"

TOKEN_EXPIRY_MINUTES = 30
ACTIVE_ACCOUNT = "Active"

ATHLETE = "Athlete"
ORCHESTRATOR = "Orchestrator"
TESTER = "Tester"
WADA = "WADA"
ADMIN = "Admin"
