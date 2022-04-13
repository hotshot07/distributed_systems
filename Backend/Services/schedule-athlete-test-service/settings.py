import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("REGION_NAME")

ATHLETE_AVAILABILITY_TABLE = 'AthleteAvailability'
ATHELTE_TEST_TABLE = 'AthleteTest'
USER_PROFILE_TABLE = 'UserProfile'
COUNTRY_ADO_TABLE = 'CountryAdo'

TEST_POSITIVE = "postive"
TEST_NEGATIVE = "negative"
TEST_INCONCLUSIVE = "inconclusive"
TEST_DID_NOT_SHOW = "did not show"
TEST_NOT_AVAILABLE = "not available"

ITEM_COULD_NOT_BE_ADDED = "Item could not be added to database"
ITEM_PARAMETERS_INVALID = "Item paramaters are invalid"
COULD_NOT_CREATE_TEST_MODEL = "Failed to create test object from provided parameters"
TRANSACTION_FAILED = "Transaction failed, check item parameters. Tester already assigned or availability slot has already been taken."
ITEM_ADDED_SUCCESSFULLY = "Item added successfully!"
ITEM_UPDATED_SUCCESSFULLY = "Item updated successfully!"
NO_UPCOMING_TESTS = "No upcoming tests"

FORM_TYPE_MUST_STRING = "Must be of type string (str)"
COUNTRIES_DONT_MATCH = "Athlete and tester are not situated in the same country"

# Roles
ATHLETE_ROLE = "Athlete"
TESTER_ROLE = "Tester"
ORCHESTRATOR_ROLE = "Orchestrator"
WADA_ROLE = "WADA"